import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

import config
from config import OUTPUT_DIR, CNPJ_DECLARANTE
from source.criar_xml_lote_assincrono import criar_xml_lote_assincrono
from source import fechamento


# =========================
# Constantes
# =========================

NS_FECHAMENTO = "http://www.eFinanceira.gov.br/schemas/evtFechamentoeFinanceira/v1_3_0"


# =========================
# Builders internos
# =========================

def _build_evt_fechamento() -> ET.Element:
    """
    Constrói o XML do evento de fechamento.
    """

    evt = fechamento.Evtfechamentoefinanceira(
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

    builder = fechamento.EvtfechamentoefinanceiraXmlBuilder()
    return builder.build(evt)


def _wrap_em_lote(xml_evt: ET.Element) -> ET.Element:
    """
    Encapsula o evento dentro do lote.
    """

    ET.register_namespace("", NS_FECHAMENTO)

    root = ET.Element(f"{{{NS_FECHAMENTO}}}eFinanceira")
    root.append(xml_evt)

    return criar_xml_lote_assincrono(
        CNPJ_DECLARANTE,
        [root]
    )


def _prettify(xml_element: ET.Element) -> str:
    """
    Formata o XML final.
    """

    xml_str = ET.tostring(xml_element, encoding="utf-8")

    return (
        minidom
        .parseString(xml_str)
        .toprettyxml(indent="  ")
        .replace("<ns0:", "<").replace("<ns1:", "<")
        .replace("</ns0:", "</").replace("</ns1:", "</")
    )


# =========================
# API pública
# =========================

def gerar_lote_fechamento(
    output_dir: str = OUTPUT_DIR,
    nome_arquivo: str = "lote_fechamento.xml"
) -> str:
    """
    Gera o XML de fechamento da e-Financeira.

    Retorna o caminho do arquivo gerado.
    """

    os.makedirs(output_dir, exist_ok=True)

    # 1. Evento
    xml_evt = _build_evt_fechamento()

    # 2. Lote
    xml_lote = _wrap_em_lote(xml_evt)

    # 3. Formatação
    xml_final = _prettify(xml_lote)

    # 4. Persistência
    output_path = os.path.join(output_dir, nome_arquivo)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(xml_final)

    print(f"[OK] Gerado {output_path}")

    return output_path


# =========================
# Execução direta
# =========================

if __name__ == "__main__":
    gerar_lote_fechamento()