import duckdb
from source.abertura import IndRetificacao
from source.criar_xml_lote_assincrono import criar_xml_lote_assincrono
from source.mov_ov_fin import *

# =========================
# Configurações
# =========================
from config import OUTPUT_DIR, CNPJ_DECLARANTE, DB_FILE, BATCH_SIZE

NS_LOTE = "http://www.eFinanceira.gov.br/schemas/envioLoteEventosAssincrono/v1_0_0"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# =========================
# XML helpers
# =========================
def pretty_xml(element: ET.Element) -> str:
    raw = ET.tostring(element, encoding="utf-8")
    return (
        minidom.parseString(raw)
        .toprettyxml(indent="  ")
        .replace("<ns0:", "<")
        .replace("</ns0:", "</")
    )


# =========================
# DuckDB: leitura do TSV
# =========================
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
    FROM '{DB_FILE}';
    """
)

handle = duckdb.sql("SELECT * FROM leitura_movimento")
schema = duckdb.sql("DESCRIBE SELECT * FROM leitura_movimento").df()
cols = schema["column_name"].tolist()

# =========================
# Geração dos lotes (somente mov op fin)
# =========================
lote_idx = 1
id_evento = 1

while batch := handle.fetchmany(BATCH_SIZE):
    lote_eventos: list[ET.Element] = []

    for row in batch:
        line = dict(zip(cols, row))

        evt = Evtmovopfin(
            id=f"ID{str(id_evento).zfill(18)}",
            ideDeclarante=Idedeclarante(
                cnpjDeclarante=Cnpjdeclarante(CNPJ_DECLARANTE),
            ),
            ideDeclarado=Idedeclarado(
                tpNI=Tpni.from_descricao(line["tpNI"]),
                NIDeclarado=Nideclarado(line["NIDeclarado"]),
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

        id_evento += 1

        xml_evt = EvtmovopfinXmlBuilder().build(evt)
        lote_eventos.append(xml_evt)

    xml_lote = criar_xml_lote_assincrono(CNPJ_DECLARANTE, lote_eventos)
    xml_final = pretty_xml(xml_lote)

    output_file = os.path.join(OUTPUT_DIR, f"lote_{str(lote_idx).zfill(4)}.xml")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(xml_final)

    print(f"[OK] Gerado {output_file} ({len(lote_eventos)} eventos)")
    lote_idx += 1
