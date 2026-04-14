"""
Módulo gerado a partir da estrutura UML do eFinanceira.
Contém as classes de Value Objects e Entidades com suas validações e
docstrings conforme a documentação original.
"""

import re
from abc import ABC, abstractmethod
from typing import Optional, Dict, Literal
import xml.etree.ElementTree as ET


# =============================================================================
#                               VALUE OBJECTS
# =============================================================================

class ID:
    """
    Cada evento da e-Financeira possui uma identificação única, gerada pela própria entidade declarante, conforme padrão
    abaixo: Exemplo: ID233390170000000000 (20 posições).

    MS1001 REGRA_VALIDA_CHAVE_ACESSO: O campo ‘id’ deve ser único na base de dados do Ambiente Nacional, para eventos
    da mesma instituição financeira e do mesmo tipo. MS1001
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
    está a ser retificado. A diferenciação da retificação entre “espontânea” e “a pedido” decorre, dentre outros motivos, da necessidade
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
    def identificar_como_original(cls) -> "IndRetificacao":
        return cls("1")

    @classmethod
    def identificar_como_retificador(cls) -> "IndRetificacao":
        return cls("2")

    @classmethod
    def identificar_como_retificador_pedido(cls) -> "IndRetificacao":
        return cls("3")

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


class TpAmb:
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
    def ambiente_de_producao(cls) -> "TpAmb":
        return cls("1")

    @classmethod
    def ambiente_de_testes(cls) -> "TpAmb":
        return cls("2")

    @classmethod
    def from_str(cls, val: Literal["1", "2"]) -> "TpAmb":
        return cls(val)

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

    @classmethod
    def from_str(cls, val: Literal["1", "2"]) -> "TipoAplicativoEmissor":
        return cls(val)


class VerAplic:
    """Este campo se destina a permitir um controle, pela própria declarante, da versão do aplicativo que
    foi utilizado para gerar o arquivo.
    """
    def __init__(self, value: str):
        if not value or not (1 <= len(value) <= 20):
            raise ValueError("Versão do aplicativo (verAplic) inválida")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "VerAplic":
        return cls(val)

    def __str__(self):
        return self.value


class CnpjDeclarante:
    """CNPJ da Entidade Declarante"""
    def __init__(self, value: str):
        if not value or not (1 <= len(value) <= 14):
            raise ValueError("CNPJ da Entidade Declarante inválido")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "CnpjDeclarante":
        return cls(val)

    def __str__(self):
        return self.value


class GIIN:
    """
    Global Intermediary Identification Number
    Neste campo deve ser informado o número do GIIN (Global Intermediary Identification Number) da entidade declarante, nos
    termos do acordo do FATCA, conforme as regras de formação descritas no sítio
    (http://www.irs.gov/PUP/businestes/corporations/giin_composition.pdf), incluindo os pontos (.) como separadores.
    Este número de cadastro na administração tributária americana deve ser obtido junto ao sítio da Receita Federal dos Estados
    Unidos (www.irs.gov/fatca) por todas as entidades sujeitas ao envio de informações no âmbito do acordo do FATCA.

    O campo deve ser informado no seguinte formato:
    6 caracteres alfanuméricos e maiúsculos (com exceção da letra "O")
    + "."
    + 5 caracteres alfanuméricos e maiúsculos (com exceção da letra "O")
    + "."
    + 2 caracteres alfabéticos e maiúsculos (que devem ser iguais a "LE", "SL",
    "ME", "BR", “SF”, “SD”, “SS”, “SB” ou "SP")
    + "."
    + 3 caracteres numéricos
    """

    def __init__(self, value: str):
        if not value or not (1 <= len(value) <= 19):
            raise ValueError("GIIN inválido")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "GIIN":
        return cls(val)

    def __str__(self):
        return self.value


class CategoriaDeclarante:
    """
    Este campo identifica os códigos de categoria de declarante, conforme o acordo do FATCA. Este campo deve ser informado
    caso a entidade declarante, nos termos do Acordo do FATCA, se enquadre como uma “Instituição Financeira Brasileira Informante”,
    independentemente se tem contas marcadas como reportável “US”. Deve-se preencher obrigatoriamente com o código
    correspondente na tabela “Categorias de Declarante”, vigente na data de recepção do evento com um dos seguintes valores:
    FATCA601, FATCA602, FATCA603, FATCA604, FATCA605, FATCA606, FATCA610 ou FATCA611.
    No caso de Instituições Financeiras Brasileiras Informantes, a Categoria de declarante é o FATCA602, pois o Brasil é uma
    Autoridade Tributária com o IGA Modelo 1 e envia as informações sobre as contas mantidas elas Instituições Brasileiras.

    REGRA_EXISTE_CATEGORIA_DECLARANTE: O valor informado no campo deverá existir na Tabela de Categoria de
    Declarante e estar vigente na data de recepção do evento (MS2019)
    """
    def __init__(self, value: str):
        if value is None:
            value = ""
        if len(value) > 8:
            raise ValueError("CategoriaDeclarante inválida: tamanho máximo é 8")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "CategoriaDeclarante":
        return cls(val)

    def __str__(self):
        return self.value


class TpInstPgto:
    """
    1 - Emissor de Instrumento de Pagamento Pos- Pago: Entidade que gerencia contas de pagamento do tipo pós-pagas, na qual os recursos são depositados pelo declarado para pagamento de débitos já assumidos.
    2 - Credenciador: Instituição de pagamento que credencia a aceitação de instrumento de pagamento.
    3 - Sub-credenciador: O participante do arranjo de pagamento que habilita usuário final recebedor para a aceitação de instrumento de pagamento
    """

    def __init__(self, value: str):
        if value not in ["1", "2", "3"]:
            raise ValueError("Tipo de Instituição de Pagamento (tpInstPgto) inválido")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "TpInstPgto":
        return cls(val)

    def __str__(self):
        return self.value


class NumeroNIF:
    """
    Número de Identificação Fiscal no Exterior
    Este grupo de informações apresenta um número de identificação fiscal emitido no exterior para a entidade declarante, se
    houver, com relação a um país para o qual ela tenha informações a serem transmitidas para fins de cumprimento do CRS. Não é
    uma informação obrigatória no leiaute, mas deve ser apresentada caso exista. O campo pode ser repetido várias vezes, para vários
    países para os quais haja informação a ser transmitida. Corresponde ao elemento “IN” do grupo de informações
    “OrganizationIN_Type”, utilizado no grupo “ReportingFI”, no esquema “CRS specific types” (“CrsXML_v.1.0.xds”).
    Para fins de CRS o número de identificação fiscal da entidade declarante junto a administração tributária transmissora
    também é informado, mas para tanto não é necessário preencher aqui novamente o CNPJ do declarante, pois essa informação já
    consta no campo “cnpjDeclarante”.
    """

    def __init__(self, value: str):
        if not value or not (1 <= len(value) <= 25):
            raise ValueError("Número NIF inválido")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "NumeroNIF":
        return cls(val)

    def __str__(self):
        return self.value


class PaisEmissao:
    """Pais de emissão do NIF"""
    def __init__(self, value: str):
        if not value or not (1 <= len(value) <= 2):
            raise ValueError("País de emissão inválido")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "PaisEmissao":
        return cls(val)

    def __str__(self):
        return self.value


class TpNIF:
    """Tipo do NIF"""
    def __init__(self, value: str):
        if not value or not (1 <= len(value) <= 30):
            raise ValueError("Tipo do NIF inválido")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "TpNIF":
        return cls(val)

    def __str__(self):
        return self.value


class Nome:
    """Nome da Entidade Declarante"""
    def __init__(self, value: str):
        if not value or not (1 <= len(value) <= 100):
            raise ValueError("Nome inválido")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Nome":
        return cls(val)

    def __str__(self):
        return self.value


class TpNome:
    """Tipo do nome da Entidade Declarante"""
    def __init__(self, value: str):
        if not value or not (1 <= len(value) <= 7):
            raise ValueError("Tipo do nome inválido")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "TpNome":
        return cls(val)

    def __str__(self):
        return self.value


class EnderecoLivre:
    """Endereço principal da Entidade Declarante"""
    def __init__(self, value: str):
        if not value or not (1 <= len(value) <= 200):
            raise ValueError("Endereço livre inválido")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "EnderecoLivre":
        return cls(val)

    def __str__(self):
        return self.value


class TpEndereco:
    """Tipo do endereço principal da Entidade Declarante"""
    def __init__(self, value: str):
        if not value or not (1 <= len(value) <= 7):
            raise ValueError("Tipo de endereço inválido")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "TpEndereco":
        return cls(val)

    def __str__(self):
        return self.value


class Municipio:
    """Código do município da Entidade Declarante"""
    def __init__(self, value: int):
        # Verifica se o número possui no máximo 7 dígitos
        if not isinstance(value, int) or len(str(value)) > 7:
            raise ValueError("Município inválido: deve ser um inteiro com até 7 dígitos")
        self.value = value

    @classmethod
    def from_int(cls, val: int) -> "Municipio":
        return cls(val)

    def __str__(self):
        return str(self.value)


class UF:
    """Sigla da Unidade da Federação da Entidade Declarante"""
    def __init__(self, value: str):
        if not value or not (1 <= len(value) <= 2):
            raise ValueError("UF inválido")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "UF":
        return cls(val)

    def __str__(self):
        return self.value


class CEP:
    """Código de Endereçamento Postal da Entidade Declarante"""
    def __init__(self, value: str):
        if not value or not (1 <= len(value) <= 8):
            raise ValueError("CEP inválido")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "CEP":
        return cls(val)

    def __str__(self):
        return self.value


class Pais:
    """País do endereço da Entidade Declarante"""
    def __init__(self, value: str):
        if not value or not (1 <= len(value) <= 2):
            raise ValueError("País inválido")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Pais":
        return cls(val)

    def __str__(self):
        return self.value


class PaisResidSigla:
    """Sigla do país de residência da Entidade Declarante"""
    def __init__(self, value: str):
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "PaisResidSigla":
        return cls(val)

    def __str__(self):
        return self.value


class EnderecoOutrosTpEndereco:
    """Tipo do endereço"""
    def __init__(self, value: str):
        # minOccurs: 0, maxLength: 7; caso seja informado, valida
        if value is not None and not (1 <= len(value) <= 7):
            raise ValueError("Tipo do endereço (EnderecoOutros_tpEndereco) inválido")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "EnderecoOutrosTpEndereco":
        return cls(val)

    def __str__(self):
        return self.value if self.value is not None else ""


class EnderecoOutrosEnderecoLivre:
    """Endereço na forma de texto livre"""
    def __init__(self, value: str):
        # minOccurs: 0, maxLength: 200; opcional
        if value is not None and not (1 <= len(value) <= 200):
            raise ValueError("EnderecoOutros_EnderecoLivre inválido")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "EnderecoOutrosEnderecoLivre":
        return cls(val)

    def __str__(self):
        return self.value if self.value is not None else ""


class EnderecoEstruturaEnderecoLivre:
    """Parte do endereço estruturado na forma de texto livre"""
    def __init__(self, value: str):
        # minOccurs: 0, maxLength: 200; opcional
        if value is not None and not (1 <= len(value) <= 200):
            raise ValueError("EnderecoEstrutura_EnderecoLivre inválido")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "EnderecoEstruturaEnderecoLivre":
        return cls(val)

    def __str__(self):
        return self.value if self.value is not None else ""


class Logradouro:
    """Logradouro"""
    def __init__(self, value: str):
        # minOccurs: 0, maxLength: 60; opcional
        if value is not None and not (1 <= len(value) <= 60):
            raise ValueError("Logradouro inválido")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Logradouro":
        return cls(val)

    def __str__(self):
        return self.value if self.value is not None else ""


class Numero:
    """Número(ou outra identificação) no logradouro"""
    def __init__(self, value: str):
        # minOccurs: 0, maxLength: 10; opcional
        if value is not None and not (1 <= len(value) <= 10):
            raise ValueError("Número inválido")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Numero":
        return cls(val)

    def __str__(self):
        return self.value if self.value is not None else ""


class Complemento:
    """Subunidade no local identificado pelo logradouro/número"""
    def __init__(self, value: str):
        # minOccurs: 0, maxLength: 10; opcional
        if value is not None and not (1 <= len(value) <= 10):
            raise ValueError("Complemento inválido")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Complemento":
        return cls(val)

    def __str__(self):
        return self.value if self.value is not None else ""


class Andar:
    """Andar da subunidade no local identificado pelo logradouro/número"""
    def __init__(self, value: str):
        # minOccurs: 0, maxLength: 10; opcional
        if value is not None and not (1 <= len(value) <= 10):
            raise ValueError("Andar inválido")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Andar":
        return cls(val)

    def __str__(self):
        return self.value if self.value is not None else ""


class Bairro:
    """Bairro(ou alguma outra subdivisão da cidade)"""
    def __init__(self, value: str):
        # minOccurs: 0, maxLength: 40; opcional
        if value is not None and not (1 <= len(value) <= 40):
            raise ValueError("Bairro inválido")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Bairro":
        return cls(val)

    def __str__(self):
        return self.value if self.value is not None else ""


class CaixaPostal:
    """Código de Caixa postal"""
    def __init__(self, value: str):
        # minOccurs: 0, maxLength: 12; opcional
        if value is not None and not (1 <= len(value) <= 12):
            raise ValueError("Caixa Postal inválido")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "CaixaPostal":
        return cls(val)

    def __str__(self):
        return self.value if self.value is not None else ""


class EnderecoEstruturaCEP:
    """Código de Endereçamento Postal do endereço"""
    def __init__(self, value: str):
        if not value or not (1 <= len(value) <= 12):
            raise ValueError("CEP do endereço estruturado inválido")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "EnderecoEstruturaCEP":
        return cls(val)

    def __str__(self):
        return self.value


class EnderecoEstruturaMunicipio:
    """Município brasileiro, ou cidade no exterior"""
    def __init__(self, value: str):
        if not value or not (1 <= len(value) <= 60):
            raise ValueError("Município do endereço estruturado inválido")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "EnderecoEstruturaMunicipio":
        return cls(val)

    def __str__(self):
        return self.value


class EnderecoEstruturaUF:
    """Unidade da Federação Brasileira (sigla) ou subdivisão do país estrangeiro"""
    def __init__(self, value: str):
        if not value or not (1 <= len(value) <= 40):
            raise ValueError("UF do endereço estruturado inválida")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "EnderecoEstruturaUF":
        return cls(val)

    def __str__(self):
        return self.value


class Signature:
    """Assinatura digital (ds:Signature)"""
    def __init__(self, value: str):
        # Considera-se que o conteúdo da assinatura seja uma string;
        # a validação específica deve ser implementada conforme necessidade.
        if not value:
            raise ValueError("Signature inválida")
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Signature":
        return cls(val)

    def __str__(self):
        return self.value

# =============================================================================
#                               ENTIDADES
# =============================================================================

class EFinanceira:
    """Elemento raiz do eFinanceira"""
    def __init__(self, evt_cad_declarante: "EvtCadDeclarante", signature: Signature):
        self.evt_cad_declarante = evt_cad_declarante
        self.signature = signature


class EvtCadDeclarante:
    """Evento de Informações da Entidade Declarante"""
    def __init__(self,
                 id: ID,
                 ide_evento: "IdeEvento",
                 ide_declarante: "IdeDeclarante",
                 info_cadastro: "InfoCadastro"):
        self.id = id
        self.ide_evento = ide_evento
        self.ide_declarante = ide_declarante
        self.info_cadastro = info_cadastro


class IdeEvento:
    """Informações de Identificação do Evento"""
    def __init__(self,
                 ind_retificacao: IndRetificacao,
                 tp_amb: TpAmb,
                 aplic_emi: TipoAplicativoEmissor,
                 ver_aplic: VerAplic,
                 nr_recibo: Optional[NumeroRecibo] = None):
        # nrRecibo é opcional (minOccurs=0)
        self.ind_retificacao = ind_retificacao
        self.nr_recibo = nr_recibo
        self.tp_amb = tp_amb
        self.aplic_emi = aplic_emi
        self.ver_aplic = ver_aplic


class IdeDeclarante:
    """Informações de identificação da Entidade Declarante"""
    def __init__(self, cnpj_declarante: CnpjDeclarante):
        self.cnpj_declarante = cnpj_declarante


class InfoCadastro:
    """Informações de cadastro da Entidade Declarante"""
    def __init__(self,
                 nome: Nome,
                 endereco_livre: EnderecoLivre,
                 municipio: Municipio,
                 uf: UF,
                 cep: CEP,
                 pais: Pais,
                 giin: Optional[GIIN] = None,
                 categoria_declarante: Optional[CategoriaDeclarante] = None,
                 info_tp_inst_pgto1: Optional["InfoTpInstPgto1"] = None,
                 nif1: Optional["NIF1"] = None,
                 tp_nome: Optional[TpNome] = None,
                 tp_endereco: Optional[TpEndereco] = None,
                 pais_resid1: Optional["PaisResid1"] = None,
                 endereco_outros1: Optional["EnderecoOutros1"] = None):
        self.giin = giin
        self.categoria_declarante = categoria_declarante
        self.info_tp_inst_pgto1 = info_tp_inst_pgto1
        self.nif1 = nif1
        self.nome = nome
        self.tp_nome = tp_nome
        self.endereco_livre = endereco_livre
        self.tp_endereco = tp_endereco
        self.municipio = municipio
        self.uf = uf
        self.cep = cep
        self.pais = pais
        self.pais_resid1 = pais_resid1
        self.endereco_outros1 = endereco_outros1


class InfoTpInstPgto1:
    """Informações do tipos de instituições de pagamento operados pelo declarante"""
    def __init__(self, tp_inst_pgto: TpInstPgto):
        self.tp_inst_pgto = tp_inst_pgto


class NIF1:
    """Informações de identificação fiscal no exterior da Entidade Declarante
    Este grupo de informações apresenta um número de identificação fiscal emitido no exterior para a entidade declarante, se
    houver, com relação a um país para o qual ela tenha informações a serem transmitidas para fins de cumprimento do CRS. Não é
    uma informação obrigatória no leiaute, mas deve ser apresentada caso exista. O campo pode ser repetido várias vezes, para vários
    países para os quais haja informação a ser transmitida. Corresponde ao elemento “IN” do grupo de informações
    “OrganizationIN_Type”, utilizado no grupo “ReportingFI”, no esquema “CRS specific types” (“CrsXML_v.1.0.xds”).
    Para fins de CRS o número de identificação fiscal da entidade declarante junto a administração tributária transmissora
    também é informado, mas para tanto não é necessário preencher aqui novamente o CNPJ do declarante, pois essa informação já
    consta no campo “cnpjDeclarante”.
    """

    def __init__(self,
                 numero_nif: NumeroNIF,
                 pais_emissao: PaisEmissao,
                 tp_nif: Optional[TpNIF] = None):
        self.numero_nif = numero_nif
        self.pais_emissao = pais_emissao
        self.tp_nif = tp_nif


class PaisResid1:
    """País de residência fiscal da Entidade Declarante"""
    def __init__(self, pais_resid_pais: PaisResidSigla):
        self.pais_resid_pais = pais_resid_pais

    def __str__(self):
        return str(self.pais_resid_pais)


class EnderecoOutros1:
    """Demais endereços da Entidade Declarante"""
    def __init__(self,
                 endereco_outros_pais: PaisResidSigla,
                 endereco_outros_tp_endereco: Optional[EnderecoOutrosTpEndereco] = None,
                 endereco_outros_endereco_livre: Optional[EnderecoOutrosEnderecoLivre] = None,
                 endereco_outros_endereco_estrutura: Optional["EnderecoOutrosEnderecoEstrutura"] = None,
                 ):
        self.endereco_outros_tp_endereco = endereco_outros_tp_endereco
        self.endereco_outros_endereco_livre = endereco_outros_endereco_livre
        self.endereco_outros_endereco_estrutura = endereco_outros_endereco_estrutura
        self.endereco_outros_pais = endereco_outros_pais

        if self.endereco_outros_endereco_livre and self.endereco_outros_endereco_estrutura:
            raise ValueError("Não é permitido informar endereço livre e endereço estruturado ao mesmo tempo.")


class EnderecoOutrosEnderecoEstrutura:
    """Endereço na forma estruturada"""
    def __init__(self,
                 endereco_estrutura_endereco_livre: Optional[EnderecoEstruturaEnderecoLivre] = None,
                 endereco: Optional["Endereco"] = None,
                 endereco_estrutura_cep: EnderecoEstruturaCEP = None,
                 endereco_estrutura_municipio: EnderecoEstruturaMunicipio = None,
                 endereco_estrutura_uf: EnderecoEstruturaUF = None):
        self.endereco_estrutura_endereco_livre = endereco_estrutura_endereco_livre
        self.endereco = endereco
        self.endereco_estrutura_cep = endereco_estrutura_cep
        self.endereco_estrutura_municipio = endereco_estrutura_municipio
        self.endereco_estrutura_uf = endereco_estrutura_uf


class Endereco:
    """Dados do endereço"""
    def __init__(self,
                 logradouro: Optional[Logradouro] = None,
                 numero: Optional[Numero] = None,
                 complemento: Optional[Complemento] = None,
                 andar: Optional[Andar] = None,
                 bairro: Optional[Bairro] = None,
                 caixa_postal: Optional[CaixaPostal] = None):
        self.logradouro = logradouro
        self.numero = numero
        self.complemento = complemento
        self.andar = andar
        self.bairro = bairro
        self.caixa_postal = caixa_postal


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


class EnderecoXmlBuilder(XmlBuilderInterface):
    def build(self, endereco: Endereco) -> ET.Element:
        el = XmlAdapter.create_element("Endereco")
        if endereco.logradouro:
            XmlAdapter.append_child(el, "Logradouro", str(endereco.logradouro))
        if endereco.numero:
            XmlAdapter.append_child(el, "Numero", str(endereco.numero))
        if endereco.complemento:
            XmlAdapter.append_child(el, "Complemento", str(endereco.complemento))
        if endereco.andar:
            XmlAdapter.append_child(el, "Andar", str(endereco.andar))
        if endereco.bairro:
            XmlAdapter.append_child(el, "Bairro", str(endereco.bairro))
        if endereco.caixa_postal:
            XmlAdapter.append_child(el, "CaixaPostal", str(endereco.caixa_postal))
        return el


class EnderecoOutrosEnderecoEstruturaXmlBuilder(XmlBuilderInterface):
    def build(self, endereco_estrutura: EnderecoOutrosEnderecoEstrutura) -> ET.Element:
        el = XmlAdapter.create_element("EnderecoEstrutura")
        if endereco_estrutura.endereco_estrutura_endereco_livre:
            XmlAdapter.append_child(el, "EnderecoLivre", str(endereco_estrutura.endereco_estrutura_endereco_livre))
        if endereco_estrutura.endereco:
            el.append(EnderecoXmlBuilder().build(endereco_estrutura.endereco))
        if endereco_estrutura.endereco_estrutura_cep:
            XmlAdapter.append_child(el, "CEP", str(endereco_estrutura.endereco_estrutura_cep))
        if endereco_estrutura.endereco_estrutura_municipio:
            XmlAdapter.append_child(el, "Municipio", str(endereco_estrutura.endereco_estrutura_municipio))
        if endereco_estrutura.endereco_estrutura_uf:
            XmlAdapter.append_child(el, "UF", str(endereco_estrutura.endereco_estrutura_uf))
        return el


class EvtCadDeclaranteXmlBuilder(XmlBuilderInterface):
    def build(self, evt_cad_declarante: EvtCadDeclarante) -> ET.Element:
        el = XmlAdapter.create_element("evtCadDeclarante", attrib={"id": str(evt_cad_declarante.id)})
        el.append(IdeEventoXmlBuilder().build(evt_cad_declarante.ide_evento))
        el.append(IdeDeclaranteXmlBuilder().build(evt_cad_declarante.ide_declarante))
        el.append(InfoCadastroXmlBuilder().build(evt_cad_declarante.info_cadastro))
        return el


class IdeEventoXmlBuilder(XmlBuilderInterface):
    def build(self, ide_evento: IdeEvento) -> ET.Element:
        el = XmlAdapter.create_element("ideEvento")
        XmlAdapter.append_child(el, "indRetificacao", str(ide_evento.ind_retificacao))
        if ide_evento.nr_recibo:
            XmlAdapter.append_child(el, "nrRecibo", str(ide_evento.nr_recibo))
        XmlAdapter.append_child(el, "tpAmb", str(ide_evento.tp_amb))
        XmlAdapter.append_child(el, "aplicEmi", str(ide_evento.aplic_emi))
        XmlAdapter.append_child(el, "verAplic", str(ide_evento.ver_aplic))
        return el


class IdeDeclaranteXmlBuilder(XmlBuilderInterface):
    def build(self, ide_declarante: IdeDeclarante) -> ET.Element:
        el = XmlAdapter.create_element("ideDeclarante")
        XmlAdapter.append_child(el, "cnpjDeclarante", str(ide_declarante.cnpj_declarante))
        return el


class InfoCadastroXmlBuilder(XmlBuilderInterface):
    def build(self, info_cadastro: InfoCadastro) -> ET.Element:
        el = XmlAdapter.create_element("infoCadastro")
        if info_cadastro.giin:
            XmlAdapter.append_child(el, "GIIN", str(info_cadastro.giin))
        if info_cadastro.categoria_declarante:
            XmlAdapter.append_child(el, "CategoriaDeclarante", str(info_cadastro.categoria_declarante))
        if info_cadastro.info_tp_inst_pgto1:
            el.append(InfoTpInstPgto1XmlBuilder().build(info_cadastro.info_tp_inst_pgto1))
        if info_cadastro.nif1:
            el.append(NIF1XmlBuilder().build(info_cadastro.nif1))
        XmlAdapter.append_child(el, "nome", str(info_cadastro.nome))
        if info_cadastro.tp_nome:
            XmlAdapter.append_child(el, "tpNome", str(info_cadastro.tp_nome))
        XmlAdapter.append_child(el, "enderecoLivre", str(info_cadastro.endereco_livre))
        if info_cadastro.tp_endereco:
            XmlAdapter.append_child(el, "tpEndereco", str(info_cadastro.tp_endereco))
        XmlAdapter.append_child(el, "municipio", str(info_cadastro.municipio))
        XmlAdapter.append_child(el, "UF", str(info_cadastro.uf))
        XmlAdapter.append_child(el, "CEP", str(info_cadastro.cep))
        XmlAdapter.append_child(el, "Pais", str(info_cadastro.pais))
        el.append(PaisResid1XmlBuilder().build(info_cadastro.pais_resid1))
        if info_cadastro.endereco_outros1:
            el.append(EnderecoOutros1XmlBuilder().build(info_cadastro.endereco_outros1))
        return el

class InfoTpInstPgto1XmlBuilder(XmlBuilderInterface):
    def build(self, info_tp_inst_pgto1: InfoTpInstPgto1) -> ET.Element:
        el = XmlAdapter.create_element("infoTpInstPgto")
        XmlAdapter.append_child(el, "tpInstPgto", str(info_tp_inst_pgto1.tp_inst_pgto))
        return el

class NIF1XmlBuilder(XmlBuilderInterface):
    def build(self, nif1: NIF1) -> ET.Element:
        el = XmlAdapter.create_element("NIF")
        XmlAdapter.append_child(el, "NumeroNIF", str(nif1.numero_nif))
        XmlAdapter.append_child(el, "PaisEmissao", str(nif1.pais_emissao))
        if nif1.tp_nif:
            XmlAdapter.append_child(el, "tpNIF", str(nif1.tp_nif))
        return el

class PaisResid1XmlBuilder(XmlBuilderInterface):
    def build(self, pais_resid1: PaisResid1) -> ET.Element:
        el = XmlAdapter.create_element("paisResid")
        XmlAdapter.append_child(el, "Pais", str(pais_resid1.pais_resid_pais))
        return el

class EnderecoOutros1XmlBuilder(XmlBuilderInterface):
    def build(self, endereco_outros1: EnderecoOutros1) -> ET.Element:
        el = XmlAdapter.create_element("EnderecoOutros")
        if endereco_outros1.endereco_outros_tp_endereco:
            XmlAdapter.append_child(el, "tpEndereco", str(endereco_outros1.endereco_outros_tp_endereco))
        if endereco_outros1.endereco_outros_endereco_livre:
            XmlAdapter.append_child(el, "EnderecoLivre", str(endereco_outros1.endereco_outros_endereco_livre))
        if endereco_outros1.endereco_outros_endereco_estrutura:
            el.append(EnderecoOutrosEnderecoEstruturaXmlBuilder().build(endereco_outros1.endereco_outros_endereco_estrutura))
        XmlAdapter.append_child(el, "Pais", str(endereco_outros1.endereco_outros_pais))
        return el

class EFinanceiraXmlBuilder(XmlBuilderInterface):
    ...


