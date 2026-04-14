import datetime
import re
from abc import ABC, abstractmethod
from typing import Optional, Dict, Literal
import xml.etree.ElementTree as ET


# ==== Value Objects ====

class DDD:
    def __init__(self, value: str):
        if not value.isdigit() or len(value) != 2:
            raise ValueError("DDD inválido")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "DDD":
        return cls(val)

    @classmethod
    def from_int(cls, val: int) -> "DDD":
        return cls(str(val).zfill(2))  # garante dois dígitos

    def __str__(self):
        return self.value


class NumeroTel:
    def __init__(self, value: str):
        if not value.isdigit() or len(value) < 8:
            raise ValueError("Número de telefone inválido")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "NumeroTel":
        return cls(val)

    @classmethod
    def from_int(cls, val: int) -> "NumeroTel":
        return cls(str(val))

    def __str__(self):
        return self.value


class Ramal:
    def __init__(self, value: str):
        if not value.isdigit():
            raise ValueError("Ramal inválido")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Ramal":
        return cls(val)

    @classmethod
    def from_int(cls, val: int) -> "Ramal":
        return cls(str(val))

    def __str__(self):
        return self.value


class CPF:
    def __init__(self, value: str):
        if not value.isdigit() or len(value) != 11:
            raise ValueError("CPF inválido")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "CPF":
        return cls(val)

    @classmethod
    def from_int(cls, val: int) -> "CPF":
        return cls(str(val).zfill(11))  # garante onze dígitos

    def __str__(self):
        return self.value


class Nome:
    def __init__(self, value: str):
        if not value or len(value) < 3:
            raise ValueError("Nome inválido")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Nome":
        return cls(val)

    def __str__(self):
        return self.value


class Setor:
    def __init__(self, value: str):
        if not value or len(value) < 3 or len(value) > 90:
            raise ValueError("Setor inválido")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Setor":
        return cls(val)

    def __str__(self):
        return self.value


class UF:
    def __init__(self, value: str):
        if len(value) != 2:
            raise ValueError("UF inválido")
        self.value = value.upper()

    @classmethod
    def from_str(cls, val: str) -> "UF":
        return cls(val)

    def __str__(self):
        return self.value


class Logradouro:
    def __init__(self, value: str):
        if not value or len(value) < 3:
            raise ValueError("Logradouro inválido")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Logradouro":
        return cls(val)

    def __str__(self):
        return self.value


class Numero:
    def __init__(self, value: str):
        if not value or len(value) < 1:
            raise ValueError("Número inválido")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Numero":
        return cls(val)

    def __str__(self):
        return self.value


class Complemento:
    def __init__(self, value: str):
        if not value or len(value) < 1:
            raise ValueError("Complemento inválido")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Complemento":
        return cls(val)

    def __str__(self):
        return self.value


class Bairro:
    def __init__(self, value: str):
        if not value or len(value) < 3:
            raise ValueError("Bairro inválido")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Bairro":
        return cls(val)

    def __str__(self):
        return self.value


class CEP:
    def __init__(self, value: str):
        if not value.isdigit() or len(value) != 8:
            raise ValueError("CEP inválido")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "CEP":
        return cls(val)

    @classmethod
    def from_int(cls, val: int) -> "CEP":
        return cls(str(val).zfill(8))  # garante oito dígitos

    def __str__(self):
        return self.value


class Municipio:
    def __init__(self, value: str):
        if not value or len(value) < 3:
            raise ValueError("Município inválido")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Municipio":
        return cls(val)

    def __str__(self):
        return self.value


class Email:
    def __init__(self, value: str):
        if "@" not in value or "." not in value:
            raise ValueError("Email inválido")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Email":
        return cls(val)

    def __str__(self):
        return self.value

class CNPJ:
    def __init__(self, value: str):
        if not value.isdigit() or len(value) != 14:
            raise ValueError("CNPJ inválido")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "CNPJ":
        return cls(val)

    @classmethod
    def from_int(cls, val: int) -> "CNPJ":
        return cls(str(val).zfill(14))  # garante quatorze dígitos

    def __str__(self):
        return self.value



class dateTypes:
    def __init__(self, value: str):
        if not value or len(value) != 10:
            raise ValueError("Data inválida")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "dateTypes":
        return cls(val)

    @classmethod
    def from_many_int(cls, ano: int, mes: int, dia: int) -> "dateTypes":
        return cls(f"{ano:04}-{mes:02}-{dia:02}")

    @classmethod
    def from_date(cls, date: datetime.date) -> "dateTypes":
        return cls(f"{date.year}-{date.month:02}-{date.day:02}")

    def __str__(self):
        return self.value


class DtInicio(dateTypes):
    def __init__(self, value: str):
        super().__init__(value)
        if not value or len(value) != 10:
            raise ValueError("Data de início inválida")
        self.value = value


class DtFim(dateTypes):
    def __init__(self, value: str):
        super().__init__(value)
        if not value or len(value) != 10:
            raise ValueError("Data de fim inválida")
        self.value = value


class CnpjDeclarante:
    def __init__(self, value: str):
        if not value.isdigit() or len(value) != 14:
            raise ValueError("CNPJ do declarante inválido")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "CnpjDeclarante":
        return cls(val)

    @classmethod
    def from_int(cls, val: int) -> "CnpjDeclarante":
        return cls(str(val).zfill(14))  # garante quatorze dígitos

    def __str__(self):
        return self.value


class IndRetificacao:
    """
    Este campo identifica se o arquivo a ser transmitido é original ou retificador de um outro arquivo válido enviado anteriormente.
    Nos casos de retificação (valor 2), é necessário informar no campo “nrRecibo” o número do recibo de entrega do arquivo que está
    sendo retificado.
    Este Evento deve ser retificado sempre que houver a necessidade de retificações de dados enviados a um período para o
    qual já foi enviado Evento de Fechamento.
    Neste caso, deve ser enviada a retificação do último Evento de Abertura válido para o período ao qual é necessária a retificação
    ou inclusão de algum novo dado, com o posterior envio dos novos eventos retificadores de movimentos compreendidos neste
    período. Para concluir, enviar a retificação do último Evento de Fechamento válido para o período a que se referem as correções.

    Exemplo:

    Fluxo normal:

    1 Envio de Evento de Abertura (Data Início 2016-01-01 e Data Fim 2016-30-06) – nrRecibo: 12345

    2 Envio de Movimentos de Operação Financeira

    3 Envio do Evento de Fechamento (Data Início 2016-01-01 e Data Fim 2016-30-06) – nrRecibo: 67890

    Necessidade de retificação ou inclusão de novos arquivos de movimento, posteriores ao __init__, para o mesmo
    período exemplificado acima:

    1 Retificação do Evento de Abertura (informar nrRecibo: 12345 e Data Início 2016-01-01 e Data Fim 2016-30-06)

    2 Envio das Retificações ou Novas Inclusões de Movimentos de Operação Financeira

    3 Retificação do Evento de Fechamento (informar nrRecibo: 67890 e Data Início 2016-01-01 e Data Fim 2016-30-06)

    ---

    Este campo identifica se o arquivo a ser transmitido é original ou retificador de um outro arquivo válido enviado anteriormente.
    No caso de retificação (opções 2 ou 3), é necessário informar no campo “nrRecibo” o número do recibo de entrega do arquivo que
    está sendo retificado. A diferenciação da retificação entre “espontânea” e “a pedido” decorre, dentre outros motivos, da necessidade
    de realizar essa distinção no momento do reporte para o cumprimento do FATCA. Assim, só deve ser utilizado o indicador “a
    pedido”, caso a retificação tenha sido solicitada pela Receita Federal, depois de detectada uma inconsistência no arquivo.
    Atentamos que não é possível o envio de dois ou mais arquivos originais para um mesmo declarado para um mesmo período
    contendo diferentes contas em cada arquivo, pois a chave do evento de movimentação financeira é:
    CNPJDeclarane+tpNI+NIDeclarado+mesAnoCaixa. Dessa forma, se a entidade enviou duas contas de um declarado, e,
    posteriormente, verificou que por algum motivo não foi enviado uma terceira conta dele, é necessário enviar um arquivo retificador
    contendo as 3 contas, mesmo que não tenha qualquer alteração nas duas contas enviadas anteriormente.
    """

    def __init__(self, value: Literal["1", "2", "3"]):
        if value not in ["1", "2", "3"]:
            raise ValueError("Indicador de retificação inválido")
        self.value = value

    @classmethod
    def identificar_como_original(cls) -> "indRetificacao":
        return cls("1")

    @classmethod
    def identificar_como_retificacao_espontanea(cls) -> "indRetificacao":
        return cls("2")

    @classmethod
    def identificar_como_retificacao_pedida(cls):
        return cls("3")

    def __str__(self):
        return self.value


class TipoAplicativoEmissor:
    """
    Este campo possibilita o controle, pela própria declarante, sobre qual aplicativo foi utilizado para gerar o arquivo (por exemplo,
    em eventuais situações de contingência em que a declarante precisou utilizar aplicativos geradores providos por terceiros).
    Caso tenha sido utilizado aplicativo gerenciado pela própria declarante, utilizar o valor “1”.
    Caso tenha sido utilizado aplicativo de terceiros, utilizar o valor “2”
    """
    def __init__(self, value: Literal["1", "2"]):
        if value not in ["1", "2"]:
            raise ValueError("Aplicativo emissor inválido")
        self.value = value

    @classmethod
    def aplicativo_proprio_do_declarante(cls) -> "TipoAplicativoEmissor":
        return cls("1")

    @classmethod
    def aplicativo_de_terceiros(cls) -> "TipoAplicativoEmissor":
        return cls("2")

    def __str__(self):
        return self.value


class VerAplic:
    """Este campo se destina a permitir um controle, pela própria declarante, da versão do aplicativo que
    foi utilizado para gerar o arquivo.
    """
    def __init__(self, value: str):
        if not value or len(value) < 1 or len(value) > 20:
            raise ValueError("Versão do aplicativo inválida")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "VerAplic":
        return cls(val)

    def __str__(self):
        return self.value


class NumeroRecibo:
    """Número do recibo do arquivo a ser retificado"""

    def __init__(self, value: str):
        padrao = '^[0-9]{1,18}-[0-9]{2}-[0-9]{3}-[0-9]{4}-[0-9]{1,18}$'

        if not value or len(value) < 1 or len(value) > 50:
            raise ValueError("Número do recibo inválido")

        if not re.match(padrao, value):
            raise ValueError("Número do recibo inválido\nFormato esperado: "
                             "\"[0-9]{1,18}-[0-9]{2}-[0-9]{3}-[0-9]{4}-[0-9]{1,18}\"")

        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "NumeroRecibo":
        return cls(val)

    def __str__(self):
        return self.value


class TipoDeAmbiente:
    """
    Este campo identifica se o evento contém informações fictícias para fins de testes dos sistemas internos dos declarantes ou
    se contém as informações que os declarantes estão obrigados a apresentar, conforme Instrução Normativa RFB nº 1.571/2015.
    Estes ambientes possuem endereços (URL) distintos.

    Eventos com as informações reais devem ser enviados apenas para o ambiente de produção com a marcação tpAmb = 1 e
    para o endereço (URL) exclusivo deste tipo de ambiente disponibilizado no item 2.2.9.3.1 (Dados para a Chamada ao Web Service
    de Envio de Lote de Eventos), ou manualmente por meio do Portal SPED na aba Serviços (Upload Manual de Arquivos) dentro do
    Módulo da e-Financeira (Página Inicial | Módulos | e-Financeira).

    Eventos com informações fictícias para testes devem ser enviados apenas para o ambiente de homologação (préprodução/testes) com a marcação tpAmb = 2 e para o endereço exclusivo deste tipo de ambiente disponibilizado no item 2.2.11.
    (Web Services de Pré-Produção).

    Se eventos com o campo tpAmb preenchido com o valor “2” forem enviados para os Web Services do ambiente de produção,
    o sistema da e-Financeira não os recepcionará, ocasionando erro no envio.
    """

    def __init__(self, value: Literal["1", "2"]):
        if value not in ["1", "2"]:
            raise ValueError("Tipo de ambiente inválido")
        self.value = value

    @classmethod
    def ambiente_de_producao(cls) -> "TipoDeAmbiente":
        return cls("1")

    @classmethod
    def ambiente_de_testes(cls) -> "TipoDeAmbiente":
        return cls("2")

    def __str__(self):
        return self.value


class ID:
    """
    Cada evento da e-Financeira possui uma identificação única, gerada pela própria entidade declarante, conforme padrão
    abaixo:
    """

    def __init__(self, value: str):
        padrao = r'^ID\d{18}$'
        if not re.match(padrao, value):
            raise ValueError("ID inválido")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "ID":
        return cls(val)

    def __str__(self):
        return self.value


# ==== Entidades ====

class Telefone:
    def __init__(self, ddd: DDD, numero: NumeroTel, ramal: Optional[Ramal] = None):
        self.ddd = ddd
        self.numero = numero
        self.ramal = ramal


class Endereco:
    def __init__(self, logradouro: Logradouro, numero: Numero, bairro: Bairro, cep: CEP, municipio: Municipio, uf: UF,
                 complemento: Optional[Complemento] = None):
        self.logradouro = logradouro
        self.numero = numero
        self.complemento = complemento
        self.bairro = bairro
        self.cep = cep
        self.municipio = municipio
        self.uf = uf


class ResponsavelEFinanceira:
    """
    Este grupo reúne informações cadastrais do responsável pela e-Financeira, ou seja, da pessoa responsável por atender
    solicitações de esclarecimentos sobre o preenchimento da e-Financeira, encaminhadas pela Receita Federal do Brasil. Pode-se
    informar mais do que um responsável.

    Caso tenha ocorrido mudança deste responsável durante o período de vigência da última abertura enviada (durante o período
    de declaração da e-Financeira), independentemente do período estar fechado ou não, deve-se retificar o “evtAberturaeFinanceira”.
    Caso o período já tenha sido fechado, após essa retificação é necessário retificar o evento de __init__ para encerrar a
    declaração novamente.

    Após informar essas mudanças na abertura de uma nova e-Financeira, não é mais necessário retificar essas informações
    nos eventos de abertura das e-Financeiras anteriores
    """

    def __init__(self, nome: Nome, cpf: CPF, telefone: Telefone, setor: Setor,
                 email: Email, endereco: Endereco):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.setor = setor
        self.endereco = endereco
        self.email = email


class IdentificacaoEntidadeDeclarante:
    """
    Este Grupo reúne informações de identificação da entidade declarante.
    """

    def __init__(self, cnpj_declarante: CnpjDeclarante):
        self.cnpj_declarante = cnpj_declarante


class ResponsavelRMF:
    """
    Este grupo reúne informações cadastrais dos responsáveis pelo atendimento à RMF (Requisição de Movimentação
    Financeira), ou seja, das pessoas Jurídicas e físicas a qual deverão ser endereçados os pedidos de RMF feitos pela Receita Federal.

    Caso tenha ocorrido mudança dos Responsáveis pela RMF da entidade declarante durante o período de vigência da última
    abertura enviada (antes de ocorrer o próximo período de declaração da e-Financeira), independentemente de este período estar
    fechado ou não, essa informação deve ser retificada por meio do “evtAberturaeFinanceira”. Após essa retificação, é necessário
    retificar o evento de __init__, caso tenha sido enviado anteriormente, para encerrar a declaração novamente. Adicionalmente,
    após informar essas mudanças na abertura de uma nova e-Financeira, não é mais necessário retificar essas informações nos
    eventos de abertura das e-Financeiras anteriores.

    Para mais informações referentes ao atendimento à RMF, consultar o site da Receita Federal, no link abaixo:
    http://idg.receita.fazenda.gov.br/orientacao/tributaria/auditoria-fiscal/rmf-orientacoes-ao-contribuinte
    """

    def __init__(self, nome: Nome, setor: Setor, telefone: Telefone, endereco: Endereco, cnpj: CNPJ,
                 cpf: CPF):
        self.cnpj = cnpj
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.setor = setor
        self.endereco = endereco


class AberturaMovOpFin:
    """
    Este grupo deve ser informado para indicar o envio de eventos de Movimentos de Operações Financeiras no período e reúne
    informações cadastrais tanto do responsável pelo atendimento às Requisições de Movimentação Financeira (RMF) endereçadas
    pela RFB à entidade quanto do representante legal da declarante.

    Para mais informações referentes ao atendimento a RMF, consultar o site da Receita Federal, no link abaixo:
    http://idg.receita.fazenda.gov.br/orientacao/tributaria/auditoria-fiscal/rmf-orientacoes-ao-contribuinte
    """

    # RepresLegal, ResponsavelRMF, RespeFin
    def __init__(self, repres_legal: "RepresLegal", responsavel_rmf: "ResponsavelRMF", respe_fin: "ResponsavelEFinanceira"):
        self.repres_legal = repres_legal
        self.responsavel_rmf = responsavel_rmf
        self.respe_fin = respe_fin


class EvtAberturaeFinanceira:
    """
    Este Evento indica a abertura do envio dos eventos de Movimento de Operações Financeiras compreendidos em um
    determinado semestre. É pré-requisito para que os eventos de Movimento de Operações Financeiras, de Movimento de Operações
    Financeiras Anual e/ou Previdência Privada sejam aceitos. Este Evento deve ser enviado a cada semestre de prestação de
    informações ou quando houver retificações de dados enviados a um período para o qual já foi enviado Evento de Fechamento.
    Neste caso, deve ser enviada a retificação do último Evento de Abertura válido para o período ao qual é necessária a retificação ou
    inclusão de algum novo dado, com o posterior envio dos novos eventos retificadores de movimentos compreendidos neste período.
    Para concluir, enviar a retificação do último Evento de Fechamento válido para o período a que se referem as correções.

    # Exemplo:

    Fluxo normal:

    - Envio de Evento de Abertura (Data Início 2016-01-01 e Data Fim 2016-30-06) – nrRecibo: 12345

    - Envio de Movimentos de Operação Financeira

    - Envio do Evento de Fechamento (Data Início 2016-01-01 e Data Fim 2016-30-06) – nrRecibo: 67890

    Necessidade de retificação ou inclusão de novos arquivos de movimento, posteriores ao __init__, para o mesmo
    período exemplificado acima:

    - Retificação do Evento de Abertura (informar nrRecibo: 12345 e Data Início 2016-01-01 e Data Fim 2016-30-06)

    - Envio das Retificações ou Novas Inclusões de Movimentos de Operação Financeira

    - Retificação do Evento de Fechamento (informar nrRecibo: 67890 e Data Início 2016-01-01 e Data Fim 2016-30-06)
    """

    def __init__(self, _id: ID, ide_evento: "IdentificaoEvento", ide_declarante: "IdentificacaoEntidadeDeclarante",
                 info_abertura: "InfoAbertura", abertura_mov_op_fin: Optional[AberturaMovOpFin] = None):
        self.id = _id
        self.ideEvento = ide_evento
        self.ideDeclarante = ide_declarante
        self.infoAbertura = info_abertura
        self.abertura_mov_op_fin = abertura_mov_op_fin



class IdentificaoEvento:
    """
    Este grupo reúne informações referentes ao evento que está sendo enviado.
    """

    def __init__(self, ind_retificacao: IndRetificacao,
                 aplic_emi: TipoAplicativoEmissor, ver_aplic: VerAplic, tp_amb: TipoDeAmbiente, nr_recibo: Optional[NumeroRecibo] = None):
        self.indRetificacao = ind_retificacao
        self.aplicEmi = aplic_emi
        self.verAplic = ver_aplic
        self.nrRecibo = nr_recibo
        self.tpAmb = tp_amb


class InfoAbertura:
    """
    Este grupo reúne informações sobre as datas de início e fim do semestre a que se referem as informações enviadas nos
    eventos de Movimento de Operações Financeiras, de Movimento de Operações Financeiras Anual e/ou Previdência Privada.
    """
    def __init__(self, dt_inicio: DtInicio, dt_fim: DtFim):
        self.dtInicio = dt_inicio
        self.dtFim = dt_fim


class RepresLegal:
    """
    Este grupo reúne informações cadastrais do representante legal da entidade declarante perante a Receita Federal.
    Caso tenha ocorrido mudança do Representante Legal da entidade declarante durante o período de vigência da última
    abertura enviada (antes de ocorrer o próximo período de declaração da e-Financeira), independentemente de este período estar
    fechado ou não, essa informação deve ser retificada por meio do “evtAberturaeFinanceira”. Após essa retificação, é necessário
    retificar o evento de __init__, caso tenha sido enviado anteriormente, para encerrar a declaração novamente. Adicionalmente,
    após informar essas mudanças na abertura de uma nova e-Financeira, não é mais necessário retificar essas informações nos
    eventos de abertura das e-Financeiras anteriores.
    """

    def __init__(self, setor: Setor, cpf: CPF, telefone: Telefone):
        # self.nome = nome
        self.setor = setor
        self.cpf = cpf
        self.telefone = telefone


# ==== Interface de XML Builder ====

class XmlBuilderInterface(ABC):
    @abstractmethod
    def build(self, obj) -> ET.Element:
        ...


# ==== Implementação do XML Builder ====

class XmlAdapter:
    @staticmethod
    def create_element(tag: str, text: Optional[str] = None, attrib: Optional[Dict[str, str]] = None) -> ET.Element:
        el = ET.Element(tag, attrib=attrib or {})
        if text is not None:
            el.text = text
        return el

    @staticmethod
    def append_child(parent: ET.Element, tag: str, text: Optional[str] = None, attrib: Optional[Dict[str, str]] = None) -> ET.Element:
        child = XmlAdapter.create_element(tag, text, attrib)
        parent.append(child)
        return child


class TelefoneXmlBuilder(XmlBuilderInterface):
    def build(self, telefone: Telefone) -> ET.Element:
        el_tel = XmlAdapter.create_element("Telefone")
        XmlAdapter.append_child(el_tel, "DDD", str(telefone.ddd))
        XmlAdapter.append_child(el_tel, "Numero", str(telefone.numero))
        if telefone.ramal:
            XmlAdapter.append_child(el_tel, "Ramal", str(telefone.ramal))
        return el_tel


class EnderecoXmlBuilder(XmlBuilderInterface):
    def build(self, endereco: Endereco) -> ET.Element:
        el_endereco = XmlAdapter.create_element("Endereco")
        XmlAdapter.append_child(el_endereco, "Logradouro", str(endereco.logradouro))
        XmlAdapter.append_child(el_endereco, "Numero", str(endereco.numero))
        if endereco.complemento:
            XmlAdapter.append_child(el_endereco, "Complemento", str(endereco.complemento))
        XmlAdapter.append_child(el_endereco, "Bairro", str(endereco.bairro))
        XmlAdapter.append_child(el_endereco, "CEP", str(endereco.cep))
        XmlAdapter.append_child(el_endereco, "Municipio", str(endereco.municipio))
        XmlAdapter.append_child(el_endereco, "UF", str(endereco.uf))
        return el_endereco


class RespeFinXmlBuilder(XmlBuilderInterface):
    def build(self, respefin: ResponsavelEFinanceira) -> ET.Element:
        el_respefin = XmlAdapter.create_element("RespeFin")
        XmlAdapter.append_child(el_respefin, "CPF", str(respefin.cpf))
        XmlAdapter.append_child(el_respefin, "Nome", str(respefin.nome))
        XmlAdapter.append_child(el_respefin, "Setor", str(respefin.setor))
        el_tel = TelefoneXmlBuilder().build(respefin.telefone)
        el_respefin.append(el_tel)
        el_endereco = EnderecoXmlBuilder().build(respefin.endereco)
        el_respefin.append(el_endereco)
        el_email = XmlAdapter.create_element("Email", str(respefin.email))
        el_respefin.append(el_email)

        return el_respefin


class ResponsavelRMFXmlBuilder(XmlBuilderInterface):
    def build(self, responsavel_rmf: ResponsavelRMF) -> ET.Element:
        el_responsavel_rmf = XmlAdapter.create_element("ResponsavelRMF")
        XmlAdapter.append_child(el_responsavel_rmf, "CNPJ", str(responsavel_rmf.cnpj))
        XmlAdapter.append_child(el_responsavel_rmf, "CPF", str(responsavel_rmf.cpf))
        XmlAdapter.append_child(el_responsavel_rmf, "Nome", str(responsavel_rmf.nome))
        XmlAdapter.append_child(el_responsavel_rmf, "Setor", str(responsavel_rmf.setor))
        el_tel = TelefoneXmlBuilder().build(responsavel_rmf.telefone)
        el_responsavel_rmf.append(el_tel)
        el_endereco = EnderecoXmlBuilder().build(responsavel_rmf.endereco)
        el_responsavel_rmf.append(el_endereco)
        return el_responsavel_rmf


class RepresLegalXmlBuilder(XmlBuilderInterface):
    def build(self, repres_legal: RepresLegal) -> ET.Element:
        el_repres_legal = XmlAdapter.create_element("RepresLegal")
        XmlAdapter.append_child(el_repres_legal, "CPF", str(repres_legal.cpf))
        XmlAdapter.append_child(el_repres_legal, "Setor", str(repres_legal.setor))
        el_tel = TelefoneXmlBuilder().build(repres_legal.telefone)
        el_repres_legal.append(el_tel)
        #XmlAdapter.append_child(el_repres_legal, "Nome", str(repres_legal.nome))
        return el_repres_legal


class AberturaMovOpFinXmlBuilder(XmlBuilderInterface):
    def build(self, abertura: AberturaMovOpFin) -> ET.Element:
        el_abertura = XmlAdapter.create_element("AberturaMovOpFin")
        el_responsavel_rmf = ResponsavelRMFXmlBuilder().build(abertura.responsavel_rmf)
        el_abertura.append(el_responsavel_rmf)
        el_respefin = RespeFinXmlBuilder().build(abertura.respe_fin)
        el_abertura.append(el_respefin)
        el_repres_legal = RepresLegalXmlBuilder().build(abertura.repres_legal)
        el_abertura.append(el_repres_legal)
        return el_abertura


class IdeDeclanteXmlBuilder(XmlBuilderInterface):
    def build(self, ide_declante: IdentificacaoEntidadeDeclarante) -> ET.Element:
        el_ide_declante = XmlAdapter.create_element("ideDeclarante")
        XmlAdapter.append_child(el_ide_declante, "cnpjDeclarante", str(ide_declante.cnpj_declarante))
        return el_ide_declante


class InfoAberturaXmlBuilder(XmlBuilderInterface):
    def build(self, info_abertura: InfoAbertura) -> ET.Element:
        el_info_abertura = XmlAdapter.create_element("infoAbertura")
        XmlAdapter.append_child(el_info_abertura, "dtInicio", str(info_abertura.dtInicio))
        XmlAdapter.append_child(el_info_abertura, "dtFim", str(info_abertura.dtFim))
        return el_info_abertura


class IdeEventoXmlBuilder(XmlBuilderInterface):
    def build(self, ide_evento: IdentificaoEvento) -> ET.Element:
        el_ide_evento = XmlAdapter.create_element("ideEvento")
        XmlAdapter.append_child(el_ide_evento, "indRetificacao", str(ide_evento.indRetificacao))
        if ide_evento.nrRecibo:
            XmlAdapter.append_child(el_ide_evento, "nrRecibo", str(ide_evento.nrRecibo))
        XmlAdapter.append_child(el_ide_evento, "tpAmb", str(ide_evento.tpAmb))
        XmlAdapter.append_child(el_ide_evento, "aplicEmi", str(ide_evento.aplicEmi))
        XmlAdapter.append_child(el_ide_evento, "verAplic", str(ide_evento.verAplic))
        return el_ide_evento


class EvtAberturaeFinanceiraXmlBuilder(XmlBuilderInterface):
    def build(self, evt_abertura: EvtAberturaeFinanceira) -> ET.Element:
        #print(evt_abertura.id)
        el_evt_abertura = XmlAdapter.create_element("evtAberturaeFinanceira", attrib={"id": str(evt_abertura.id)})
        el_ide_evento = IdeEventoXmlBuilder().build(evt_abertura.ideEvento)
        el_evt_abertura.append(el_ide_evento)
        el_ide_declarante = IdeDeclanteXmlBuilder().build(evt_abertura.ideDeclarante)
        el_evt_abertura.append(el_ide_declarante)
        el_info_abertura = InfoAberturaXmlBuilder().build(evt_abertura.infoAbertura)
        el_evt_abertura.append(el_info_abertura)
        if evt_abertura.abertura_mov_op_fin:
            el_abertura_mov_op_fin = AberturaMovOpFinXmlBuilder().build(evt_abertura.abertura_mov_op_fin)
            el_evt_abertura.append(el_abertura_mov_op_fin)
        return el_evt_abertura


