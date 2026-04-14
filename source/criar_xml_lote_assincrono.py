from xml.etree import ElementTree
import xml.etree.ElementTree as ET
import config
from config import NS_LOTE


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

    for evt in eventos_evt_mov_op_fin:
        evento_el = ET.SubElement(
            eventos_el,
            f"{{{NS_LOTE}}}evento",
            {"id": f"ID{str(config.evt_id_count).zfill(18)}"},
        )
        config.evt_id_count += 1
        evento_el.append(evt)

    return root
