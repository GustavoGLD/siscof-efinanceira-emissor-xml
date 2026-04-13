import os
import re
import duckdb
import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import Generator, Iterable

from config import OUTPUT_DIR, CNPJ_DECLARANTE, DB_FILE, BATCH_SIZE
from source.abertura import IndRetificacao
from source.criar_xml_lote_assincrono import criar_xml_lote_assincrono
from source.mov_ov_fin import *


# =========================
# Constantes
# =========================

NS_LOTE = "http://www.eFinanceira.gov.br/schemas/envioLoteEventosAssincrono/v1_0_0"


# =========================
# XML helpers
# =========================

def _pretty_xml(element: ET.Element) -> str:
    raw = ET.tostring(element, encoding="utf-8")
    return (
        minidom.parseString(raw)
        .toprettyxml(indent="  ")
        .replace("<ns0:", "<")
        .replace("</ns0:", "</")
    )


# =========================
# DuckDB (infra)
# =========================

def _init_duckdb(db_file: str):
    duckdb.sql(
        f"""
        CREATE OR REPLACE TABLE leitura_movimento (
            tpNI            VARCHAR,
            NIDeclarado     VARCHAR,
            NomeDeclarado   VARCHAR,
            EnderecoLivre   VARCHAR,
            numConta        VARCHAR,
            anoMesCaixa     VARCHAR,
            totCreditos     DECIMAL(10,2),
            totDebitos      DECIMAL(10,2),
            totPgtosAcum    DECIMAL(10,2)
        );

        COPY leitura_movimento
        FROM '{db_file}';
        """
    )


def _stream_batches(batch_size: int) -> Generator[list[dict], None, None]:
    handle = duckdb.sql("SELECT * FROM leitura_movimento")
    schema = duckdb.sql("DESCRIBE SELECT * FROM leitura_movimento").df()
    cols = schema["column_name"].tolist()

    while batch := handle.fetchmany(batch_size):
        yield [dict(zip(cols, row)) for row in batch]


# =========================
# Transformação (core)
# =========================

def _build_evt_from_row(line: dict, id_evento: int) -> ET.Element:
    """
    Converte uma linha do TSV em um evento XML.
    """

    evt = Evtmovopfin(
        id=f"ID{str(id_evento).zfill(18)}",
        ideDeclarante=Idedeclarante(
            cnpjDeclarante=Cnpjdeclarante(CNPJ_DECLARANTE),
        ),
        ideDeclarado=Idedeclarado(
            tpNI=Tpni.from_str(line["tpNI"]),
            NIDeclarado=Nideclarado(re.sub('[^0-9]', '', line["NIDeclarado"])),
            PaisEndereco=Paisendereco(Pais("BR")),
            NomeDeclarado=Nomedeclarado(line["NomeDeclarado"]),
            tpDeclarado=None,
            NIF=None,
            tpNomeDeclarado=None,
            NomeOutros=None,
            DataNasc=None,
            InfoNascimento=None,
            EnderecoLivre=Enderecolivre(line["EnderecoLivre"]),
            tpEndereco=None,
            EnderecoOutros=None,
            paisResid=None,
            PaisNacionalidade=None,
            Proprietarios=None,
        ),
        mesCaixa=Mescaixa(
            Anomescaixa(line["anoMesCaixa"]),
            Movopfin(
                Conta=[
                    Conta(
                        infoConta=Infoconta(
                            BalancoConta=Balancoconta(
                                totCreditos=Totcreditos.from_decimal(line["totCreditos"]),
                                totDebitos=Totdebitos.from_decimal(line["totDebitos"]),
                                totCreditosMesmaTitularidade=Totcreditosmesmatitularidade("0,00"),
                                totDebitosMesmaTitularidade=Totdebitosmesmatitularidade("0,00"),
                                vlrUltDia=None,
                            ),
                            PgtosAcum=[
                                Pgtosacum(
                                    tpPgto=[Tppgto("CRS504")],
                                    totPgtosAcum=Totpgtosacum.from_decimal(line["totPgtosAcum"]),
                                )
                            ],
                            tpConta=Tpconta("1"),
                            subTpConta=Subtpconta("106"),
                            tpNumConta=Tpnumconta("OECD605"),
                            numConta=Numconta(line["numConta"]),
                            tpRelacaoDeclarado=Tprelacaodeclarado("1"),
                            moeda=Moeda("BRL"),
                            Intermediario=None,
                            NoTitulares=None,
                            dtEncerramentoConta=None,
                            IndInatividade=None,
                            IndNDoc=None,
                            Fundo=None,
                            Reportavel=[Reportavel(Pais("BR"))],
                        ),
                        MedJudic=None,
                    )
                ],
                Cambio=None,
            ),
        ),
        ideEvento=Ideevento(
            # sem abertura/fechamento: mantemos o evento como ORIGINAL
            indRetificacao=IndRetificacao.identificar_como_original(),
            nrRecibo=None,
            tpAmb=Tpamb("2"),
            aplicEmi=Aplicemi("2"),
            verAplic=Veraplic("1.0"),
        ),
    )

    return EvtmovopfinXmlBuilder().build(evt)


# =========================
# Lote (application)
# =========================

def _gerar_lote(
    eventos: Iterable[ET.Element],
) -> ET.Element:
    return criar_xml_lote_assincrono(CNPJ_DECLARANTE, list(eventos))


def _salvar_lote(xml_element: ET.Element, path: str):
    xml_final = _pretty_xml(xml_element)

    with open(path, "w", encoding="utf-8") as f:
        f.write(xml_final)


# =========================
# API pública (pipeline)
# =========================

def gerar_lotes_movimento(
    db_file: str = DB_FILE,
    batch_size: int = BATCH_SIZE,
    output_dir: str = OUTPUT_DIR,
) -> list[str]:
    """
    Pipeline completo:
    TSV -> DuckDB -> Eventos -> Lotes XML

    Retorna lista de arquivos gerados.
    """

    os.makedirs(output_dir, exist_ok=True)

    _init_duckdb(db_file)

    arquivos_gerados = []
    id_evento = 1
    lote_idx = 1

    for batch in _stream_batches(batch_size):

        eventos = []
        for line in batch:
            xml_evt = _build_evt_from_row(line, id_evento)
            eventos.append(xml_evt)
            id_evento += 1

        xml_lote = _gerar_lote(eventos)

        output_file = os.path.join(
            output_dir,
            f"lote_{str(lote_idx).zfill(4)}.xml"
        )

        _salvar_lote(xml_lote, output_file)

        print(f"[OK] {output_file} ({len(eventos)} eventos)")

        arquivos_gerados.append(output_file)
        lote_idx += 1

    return arquivos_gerados


# =========================
# Execução direta
# =========================

if __name__ == "__main__":
    gerar_lotes_movimento()