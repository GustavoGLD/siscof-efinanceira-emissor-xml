import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

from config import OUTPUT_DIR
from source.abertura import *
from source.abertura import IndRetificacao
from source.criar_xml_lote_assincrono import criar_xml_lote_assincrono


# =========================
# Constantes
# =========================

NS_EVT = "http://www.eFinanceira.gov.br/schemas/evtMovOpFin/v1_2_1"
NS_ABERTURA = "http://www.eFinanceira.gov.br/schemas/evtAberturaeFinanceira/v1_2_1"


# =========================
# Builders internos
# =========================

def _build_evt_abertura(
    cnpj_declarante: str,
) -> ET.Element:
    """
    Constrói o XML do evento de abertura.
    """

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
            cnpj_declarante=CnpjDeclarante(cnpj_declarante)
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
    return builder.build(evt_abertura)


def _wrap_em_lote(
    cnpj_declarante: str,
    xml_evt: ET.Element
) -> ET.Element:
    """
    Encapsula o evento dentro do lote assíncrono.
    """

    ET.register_namespace("", NS_ABERTURA)

    root = ET.Element(f"{{{NS_ABERTURA}}}eFinanceira")
    root.append(xml_evt)

    return criar_xml_lote_assincrono(
        cnpj_declarante,
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
# API pública do módulo
# =========================

def gerar_lote_abertura(
    cnpj_declarante: str,
    output_path: str | None = None,
    nome_arquivo: str = "lote_abertura.xml"
) -> str:
    """
    Gera o XML de lote de abertura da e-Financeira.

    Retorna o caminho do arquivo gerado.
    """

    if output_path is None:
        output_path = OUTPUT_DIR

    os.makedirs(output_path, exist_ok=True)

    # 1. Construir evento
    xml_evt = _build_evt_abertura(cnpj_declarante)

    # 2. Envelopar em lote
    xml_lote = _wrap_em_lote(cnpj_declarante, xml_evt)

    # 3. Formatar
    xml_final = _prettify(xml_lote)

    # 4. Persistir
    file_path = os.path.join(output_path, nome_arquivo)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(xml_final)

    return file_path


# =========================
# Execução direta (opcional)
# =========================

if __name__ == "__main__":
    from config import CNPJ_DECLARANTE, OUTPUT_DIR

    path = gerar_lote_abertura(CNPJ_DECLARANTE, OUTPUT_DIR)
    print(f"XML gerado em: {path}")