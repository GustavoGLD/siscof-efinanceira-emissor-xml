import os
from xml.dom import minidom

from config import OUTPUT_DIR, CNPJ_DECLARANTE
from source.abertura import *
from source.abertura import IndRetificacao
from source.criar_xml_lote_assincrono import criar_xml_lote_assincrono

# =========================
# Configurações
# =========================

NOME_ARQUIVO_OUTPUT = "lote_abertura.xml"
os.makedirs(OUTPUT_DIR, exist_ok=True)

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
    os.path.join(OUTPUT_DIR, NOME_ARQUIVO_OUTPUT),
    "w",
    encoding="utf-8"
) as f:
    f.write(xml_final)

