import os
from xml.dom import minidom

import config
from config import OUTPUT_DIR, CNPJ_DECLARANTE
from source.abertura import *
from source.criar_xml_lote_assincrono import criar_xml_lote_assincrono

# =========================
# Configurações
# =========================

NOME_ARQUIVO_OUTPUT = "lote_fechamento.xml"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# Evento de Fechamento
# =========================
from source import fechamento

evt_fechamento = fechamento.Evtfechamentoefinanceira(
    id=f"ID{str(config.evt_id_count).zfill(18)}",
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

output_fechamento = os.path.join(OUTPUT_DIR, NOME_ARQUIVO_OUTPUT)

with open(output_fechamento, "w", encoding="utf-8") as f:
    f.write(xml_final_fechamento)

print("[OK] Gerado lote_fechamento.xml")