import duckdb
import os
from xml.dom import minidom
import xml.etree.ElementTree as ET

from source.abertura import *
from source.abertura import IndRetificacao


# =========================
# Configurações
# =========================

DB_FILE = "movimentacao-dados.tsv"
BATCH_SIZE = 50
OUTPUT_DIR = "out"
CNPJ_DECLARANTE = "14115686000170"

NS_LOTE = "http://www.eFinanceira.gov.br/schemas/envioLoteEventosAssincrono/v1_0_0"

evt_id_count = 0

os.makedirs(OUTPUT_DIR, exist_ok=True)

def criar_xml_lote_assincrono(
    cnpj_declarante: str,
    eventos_evt_mov_op_fin: list[ET.Element],
) -> ET.Element:

    if not eventos_evt_mov_op_fin:
        raise ValueError("Lista de eventos não pode ser vazia")

    if len(eventos_evt_mov_op_fin) > 50:
        raise ValueError("Máximo de 50 eventos por lote")

    ET.register_namespace("", NS_LOTE)

    root = ET.Element(f"{{{NS_LOTE}}}eFinanceira")
    lote = ET.SubElement(root, f"{{{NS_LOTE}}}loteEventosAssincrono")

    cnpj_el = ET.SubElement(lote, f"{{{NS_LOTE}}}cnpjDeclarante")
    cnpj_el.text = cnpj_declarante

    eventos_el = ET.SubElement(lote, f"{{{NS_LOTE}}}eventos")

    global evt_id_count
    for evt in eventos_evt_mov_op_fin:
        evento_el = ET.SubElement(
            eventos_el,
            f"{{{NS_LOTE}}}evento",
            {"id": f"ID{str(evt_id_count).zfill(18)}"},
        )
        evt_id_count += 1
        evento_el.append(evt)

    return root


# =========================
# Evento de Abertura
# =========================

NS_EVT = "http://www.eFinanceira.gov.br/schemas/evtMovOpFin/v1_2_1"

evt_abertura = EvtAberturaeFinanceira(
    _id=ID("ID000000000000000000"),
    ide_evento=IdentificaoEvento(
        ind_retificacao=IndRetificacao.identificar_como_original(),
        aplic_emi=TipoAplicativoEmissor.aplicativo_de_terceiros(),
        ver_aplic=VerAplic("1.0"),
        nr_recibo=NumeroRecibo("12345-12-345-6789-67890"),
        tp_amb=TipoDeAmbiente.ambiente_de_testes()
    ),
    ide_declarante=IdentificacaoEntidadeDeclarante(
        cnpj_declarante=CnpjDeclarante(CNPJ_DECLARANTE)
    ),
    info_abertura=InfoAbertura(
        dt_inicio=DtInicio("2023-01-01"),
        dt_fim=DtFim("2023-06-30")
    ),
    abertura_mov_op_fin=AberturaMovOpFin(
        repres_legal=RepresLegal(
            setor=Setor("Financeiro"),
            cpf=CPF("83358633187"),
            telefone=Telefone(
                ddd=DDD("65"),
                numero=NumeroTel("999017193"),
            )
        ),
        responsavel_rmf=ResponsavelRMF(
            nome=Nome("WERIKA CALASSA"),
            cpf=CPF("83358633187"),
            telefone=Telefone(
                ddd=DDD("65"),
                numero=NumeroTel("999017193"),
            ),
            setor=Setor("Financeiro"),
            endereco=Endereco(
                logradouro=Logradouro("Avenida Sagitário"),
                numero=Numero("138"),
                complemento=Complemento("Conjunto 312"),
                bairro=Bairro("Bairro Sítio Tamboré/Alphaville"),
                cep=CEP("06473073"),
                municipio=Municipio("Barueri"),
                uf=UF("SP")
            ),
            cnpj=CNPJ("47377613000106")
        ),
        respe_fin=ResponsavelEFinanceira(
            nome=Nome("WERIKA CALASSA"),
            cpf=CPF("83358633187"),
            telefone=Telefone(
                ddd=DDD("11"),
                numero=NumeroTel("987654321"),
                ramal=None
            ),
            setor=Setor("Financeiro"),
            email=Email("gustavo@gmail.com"),
            endereco=Endereco(
                logradouro=Logradouro("Avenida Sagitário"),
                numero=Numero("138"),
                complemento=Complemento("Conjunto 312"),
                bairro=Bairro("Bairro Sítio Tamboré/Alphaville"),
                cep=CEP("06473073"),
                municipio=Municipio("Barueri"),
                uf=UF("SP")
            )
        )
    )
)
builder = EvtAberturaeFinanceiraXmlBuilder()

# =========================
# Lote exclusivo da abertura
# =========================

NS = "http://www.eFinanceira.gov.br/schemas/evtAberturaeFinanceira/v1_2_1"
ET.register_namespace("", NS)

# elemento evtAbertura já construído pelo builder
xml_abertura = builder.build(evt_abertura)

# root <eFinanceira>
root = ET.Element(f"{{{NS}}}eFinanceira")
root.append(xml_abertura)

xml_lote_abertura = criar_xml_lote_assincrono(
    CNPJ_DECLARANTE,
    [root]
)

xml_final = (
    minidom
    .parseString(ET.tostring(xml_lote_abertura, encoding="utf-8"))
    .toprettyxml(indent="  ")
    .replace("<ns0:", "<").replace("<ns1:", "<")
    .replace("</ns0:", "</").replace("</ns1:", "</")
)

with open(
    os.path.join(OUTPUT_DIR, "lote_abertura.xml"),
    "w",
    encoding="utf-8"
) as f:
    f.write(xml_final)


# =========================
# Inicialização
# =========================

from source.mov_ov_fin import *

print("[OK] Gerado lote_abertura.xml")

os.makedirs(OUTPUT_DIR, exist_ok=True)

duckdb.sql(f"""
CREATE OR REPLACE TABLE leitura_movimento (
    tpNI            VARCHAR,
    NIDeclarado     VARCHAR,
    NomeDeclarado   VARCHAR,
    EnderecoLivre  VARCHAR,
    numConta        VARCHAR,
    anoMesCaixa     VARCHAR,
    totCreditos    DECIMAL(10,2),
    totDebitos     DECIMAL(10,2),
    totPgtosAcum   DECIMAL(10,2)
);
COPY leitura_movimento
FROM '{DB_FILE}';
""")
handle = duckdb.sql("SELECT * FROM leitura_movimento")
schema = duckdb.sql("DESCRIBE SELECT * FROM leitura_movimento").df()


# =========================
# Funções auxiliares
# =========================

cols = schema["column_name"].tolist()


def pretty_xml(element: ET.Element) -> str:
    raw = ET.tostring(element, encoding="utf-8")
    return (
        minidom
        .parseString(raw)
        .toprettyxml(indent="  ")
        .replace("<ns0:", "<")
        .replace("</ns0:", "</")
    )


# =========================
# Geração dos lotes
# =========================

lote_idx = 1
id_evento = 1

while batch := handle.fetchmany(BATCH_SIZE):
    lote_eventos = []

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
                                        totPgtosAcum=Totpgtosacum.from_decimal(
                                            line["totPgtosAcum"]
                                        ),
                                    )
                                ],
                                tpConta=Tpconta("1"),
                                subTpConta=Subtpconta("199"),
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

    output_file = os.path.join(
        OUTPUT_DIR,
        f"lote_{str(lote_idx).zfill(4)}.xml"
    )

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(xml_final)

    print(f"[OK] Gerado {output_file} ({len(lote_eventos)} eventos)")
    lote_idx += 1


# =========================
# Evento de Fechamento
# =========================
from source import fechamento

evt_fechamento = fechamento.Evtfechamentoefinanceira(
    id=f"ID{str(id_evento).zfill(18)}",
    ideEvento=fechamento.Ideevento(
        indRetificacao=fechamento.Indretificacao("1"),
        nrRecibo=None,
        tpAmb=fechamento.Tpamb("1"),
        aplicEmi=fechamento.Aplicemi("1"),
        verAplic=fechamento.Veraplic("1.0"),
    ),

    ideDeclarante=fechamento.Idedeclarante(
        cnpjDeclarante=fechamento.Cnpjdeclarante(CNPJ_DECLARANTE)
    ),

    infoFechamento=fechamento.Infofechamento(
        dtInicio=fechamento.Dtinicio("2024-01-01"),
        dtFim=fechamento.Dtfim("2024-12-31"),
        sitEspecial=fechamento.Sitespecial("0"),
        nadaADeclarar=None,
    ),

    FechamentoPP=None,
    FechamentoMovOpFin=None,
    FechamentoMovOpFinAnual=None,
)

builder_fechamento = fechamento.EvtfechamentoefinanceiraXmlBuilder()

NS = "http://www.eFinanceira.gov.br/schemas/evtFechamentoeFinanceira/v1_3_0"
ET.register_namespace("", NS)  # evita prefixos tipo ns0

xml_fechamento: ET.Element = builder_fechamento.build(evt_fechamento)

root = ET.Element(f"{{{NS}}}eFinanceira")

root.append(xml_fechamento)


# =========================
# Lote exclusivo do fechamento
# =========================
xml_lote_fechamento = criar_xml_lote_assincrono(
    CNPJ_DECLARANTE,
    [root]
)

xml_final_fechamento = (
    minidom
    .parseString(ET.tostring(xml_lote_fechamento, encoding="utf-8"))
    .toprettyxml(indent="  ")
    .replace("<ns0:", "<").replace("<ns1:", "<")
    .replace("</ns0:", "</").replace("</ns1:", "</")
)

output_fechamento = os.path.join(OUTPUT_DIR, "lote_fechamento.xml")

with open(output_fechamento, "w", encoding="utf-8") as f:
    f.write(xml_final_fechamento)

print("[OK] Gerado lote_fechamento.xml")
