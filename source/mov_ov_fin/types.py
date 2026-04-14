import re
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional, List, Literal


class Indretificacao:
    """"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Indretificacao":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Nrrecibo:
    """"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Nrrecibo":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Tpamb:
    """"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Tpamb":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Aplicemi:
    """"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Aplicemi":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Veraplic:
    """"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Veraplic":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Cnpjdeclarante:
    """CNPJ da Entidade Declarante"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Cnpjdeclarante":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Tpni:
    """Tipo de NI"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Tpni":
        return cls(val)

    @classmethod
    def from_descricao(cls, val: str) -> "Tpni":
        if val.upper() == "CPF":
            return cls("1")
        elif val.upper() == "CNPJ":
            return cls("2")
        else:
            raise ValueError(f'A descrição de TpNI deve ser "CPF" ou "CNPJ", e não: "{val}"')

    def __str__(self):
        return str(self.value)


class Tpdeclarado:
    """Tipo para fins de intercambio de informacoes"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Tpdeclarado":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Nideclarado:
    """NI"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Nideclarado":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Numeronif:
    """Numero de Identificacao Fiscal"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Numeronif":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Paisemissaonif:
    """Pais de emissao do Numero de Identificacao Fiscal"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Paisemissaonif":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Tpnif:
    """Tipo do Numero de Identificacao Fiscal"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Tpnif":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Nomedeclarado:
    """Nome"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Nomedeclarado":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Tpnomedeclarado:
    """Tipo do Nome"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Tpnomedeclarado":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Tpnome:
    """Tipo do nome"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Tpnome":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Prectitulo:
    """Informacao que precede ao titulo do nome (ex: vossa excelencia, espolio de)"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Prectitulo":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Titulo:
    """Titulo do nome (ex: sr., sra.)"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Titulo":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Tipo:
    """Tipo do primeiro nome (ex: nome proprio, nome de batismo)"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Tipo":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Nome:
    """Primeiro nome"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Nome":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Idgeracao:
    """Parte do nome indicativa de geracao (ex: junior, neto, III)"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Idgeracao":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Sufixo:
    """Siglas credenciais do nome (ex: PhD, VQ, QC)"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Sufixo":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Gensufixo:
    """Indicativo associado ao nome (ex: falecido, aposentado)"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Gensufixo":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Datanasc:
    """Data de nascimento Formato: AAAA-MM-DD"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Datanasc":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Municipio:
    """Municipio brasileiro (ou cidade no exterior) do local do nascimento"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Municipio":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Bairro:
    """Bairro (ou alguma outra subdivisao da cidade) do local do nascimento"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Bairro":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Pais:
    """Pais de nascimento do declarado, conforme tabela de paises"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Pais":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Antigonomepais:
    """Pais de nascimento (por extenso), no caso de pais extinto"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Antigonomepais":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Enderecolivre:
    """Endereco principal do declarado"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Enderecolivre":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Tpendereco:
    """"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Tpendereco":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Logradouro:
    """"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Logradouro":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Numero:
    """"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Numero":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Complemento:
    """"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Complemento":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Andar:
    """"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Andar":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Caixapostal:
    """"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Caixapostal":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Cep:
    """"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Cep":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Uf:
    """"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Uf":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Niproprietario:
    """Numero de Identificacao (NI)"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Niproprietario":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Tpproprietario:
    """Tipo de Proprietario"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Tpproprietario":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Anomescaixa:
    """Mes caixa que esta sendo reportado"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Anomescaixa":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Numprocjud:
    """"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Numprocjud":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Vara:
    """Vara de tramitacao"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Vara":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Secjud:
    """Secao judiciaria"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Secjud":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Subsecjud:
    """Subsecao judiciaria"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Subsecjud":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Dtconcessao:
    """Data da concessao"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Dtconcessao":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Dtcassacao:
    """Data da cassacao"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Dtcassacao":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Tpconta:
    """Tipo de conta"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Tpconta":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Subtpconta:
    """Subtipo de conta"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Subtpconta":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Tpnumconta:
    """Tipo do numero da conta"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Tpnumconta":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Numconta:
    """Numero da conta"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Numconta":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Tprelacaodeclarado:
    """Tipo de relacao do declarado"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Tprelacaodeclarado":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Moeda:
    """Moeda na qual os valores de movimentacao da conta serao informados"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Moeda":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Giin:
    """GIIN (Global Intermediary Identification Number)"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Giin":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Niintermediario:
    """NI"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Niintermediario":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Notitulares:
    """Numero de titulares da conta"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Notitulares":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Dtencerramentoconta:
    """Data de encerramento da conta"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Dtencerramentoconta":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Indinatividade:
    """Indicador de inatividade da conta"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Indinatividade":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Indndoc:
    """Indicador de conta nao documentada"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Indndoc":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Cnpj:
    """CNPJ referente ao fundo de investimentos"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Cnpj":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Totcreditos:
    """Total de creditos"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Totcreditos":
        return cls(val)

    @classmethod
    def from_decimal(cls, val: Decimal) -> "Totcreditos":
        v = val.quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
        s = format(v, "f").replace(".", ",")
        return cls(s)

    def __str__(self):
        return str(self.value)


class Totdebitos:
    """Total de debitos"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_decimal(cls, val: Decimal) -> "Totdebitos":
        s = format(val, "f").replace(".", ",")
        return cls(s)

    def __str__(self):
        return str(self.value)


class Totcreditosmesmatitularidade:
    """Total de creditos do mesmo titular"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Totcreditosmesmatitularidade":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Totdebitosmesmatitularidade:
    """Total de debitos do mesmo titular"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Totdebitosmesmatitularidade":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Vlrultdia:
    """Saldo no ultimo dia do mes"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Vlrultdia":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Tppgto:
    """Tipo de pagamento"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Tppgto":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Totpgtosacum:
    """Total acumulado de pagamentos realizados no ano"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Totpgtosacum":
        return cls(val)

    @classmethod
    def from_decimal(cls, val: Decimal) -> "Totpgtosacum":
        v = val.quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
        s = format(v, "f").replace(".", ",")
        return cls(s)


    def __str__(self):
        return str(self.value)


class Totcompras:
    """Valor total de compras"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Totcompras":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Totvendas:
    """Valor total de vendas"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Totvendas":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Tottransferencias:
    """Valor total de transferencias"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Tottransferencias":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Efinanceira:
    """"""
    def __init__(self, evtMovOpFin: "Evtmovopfin", Signature: "Signature"):
        self.evtMovOpFin = evtMovOpFin
        self.Signature = Signature


class Evtmovopfin:
    """Evento de Informacoes de Movimento de Operacoes Financeiras"""
    def __init__(self, id: str, ideEvento: "Ideevento", ideDeclarante: "Idedeclarante", ideDeclarado: "Idedeclarado", mesCaixa: "Mescaixa"):
        self.id = id
        self.ideEvento = ideEvento
        self.ideDeclarante = ideDeclarante
        self.ideDeclarado = ideDeclarado
        self.mesCaixa = mesCaixa


class Ideevento:
    """Identificacao do evento"""
    def __init__(self, indRetificacao: "Indretificacao", nrRecibo: Optional["Nrrecibo"], tpAmb: "Tpamb", aplicEmi: "Aplicemi", verAplic: "Veraplic"):
        self.indRetificacao = indRetificacao
        self.nrRecibo = nrRecibo
        self.tpAmb = tpAmb
        self.aplicEmi = aplicEmi
        self.verAplic = verAplic


class Idedeclarante:
    """"""
    def __init__(self, cnpjDeclarante: "Cnpjdeclarante"):
        self.cnpjDeclarante = cnpjDeclarante


class Idedeclarado:
    """"""
    def __init__(self, tpNI: "Tpni", tpDeclarado: Optional[List["Tpdeclarado"]], NIDeclarado: "Nideclarado", NIF: Optional[List["Nif"]], NomeDeclarado: "Nomedeclarado", tpNomeDeclarado: Optional["Tpnomedeclarado"], NomeOutros: Optional[List["Nomeoutros"]], DataNasc: Optional["Datanasc"], InfoNascimento: Optional["Infonascimento"], EnderecoLivre: Optional["Enderecolivre"], tpEndereco: Optional["Tpendereco"], PaisEndereco: "Paisendereco", EnderecoOutros: Optional[List["Enderecooutros"]], paisResid: Optional[List["Paisresid"]], PaisNacionalidade: Optional[List["Paisnacionalidade"]], Proprietarios: Optional[List["Proprietarios"]]):
        self.tpNI = tpNI
        self.tpDeclarado = tpDeclarado
        self.NIDeclarado = NIDeclarado
        self.NIF = NIF
        self.NomeDeclarado = NomeDeclarado
        self.tpNomeDeclarado = tpNomeDeclarado
        self.NomeOutros = NomeOutros
        self.DataNasc = DataNasc
        self.InfoNascimento = InfoNascimento
        self.EnderecoLivre = EnderecoLivre
        self.tpEndereco = tpEndereco
        self.PaisEndereco = PaisEndereco
        self.EnderecoOutros = EnderecoOutros
        self.paisResid = paisResid
        self.PaisNacionalidade = PaisNacionalidade
        self.Proprietarios = Proprietarios


class Nif:
    """Numero de Identificacao Fiscal no Exterior"""
    def __init__(self, NumeroNIF: "Numeronif", PaisEmissaoNIF: "Paisemissaonif", tpNIF: Optional["Tpnif"]):
        self.NumeroNIF = NumeroNIF
        self.PaisEmissaoNIF = PaisEmissaoNIF
        self.tpNIF = tpNIF


class Nomeoutros:
    """Demais nomes do declarado"""
    def __init__(self, NomePF: Optional["Nomepf"], NomePJ: Optional["Nomepj"]):
        self.NomePF = NomePF
        self.NomePJ = NomePJ


class Nomepf:
    """Nome de Pessoa Fisica"""
    def __init__(self, tpNome: Optional["Tpnome"], PrecTitulo: Optional["Prectitulo"], Titulo: Optional[List["Titulo"]], PrimeiroNome: "Primeironome", MeioNome: Optional[List["Meionome"]], PrefixoNome: Optional["Prefixonome"], UltimoNome: "Ultimonome", IdGeracao: Optional[List["Idgeracao"]], Sufixo: Optional[List["Sufixo"]], GenSufixo: Optional["Gensufixo"]):
        self.tpNome = tpNome
        self.PrecTitulo = PrecTitulo
        self.Titulo = Titulo
        self.PrimeiroNome = PrimeiroNome
        self.MeioNome = MeioNome
        self.PrefixoNome = PrefixoNome
        self.UltimoNome = UltimoNome
        self.IdGeracao = IdGeracao
        self.Sufixo = Sufixo
        self.GenSufixo = GenSufixo


class Primeironome:
    """Informacao do primeiro nome"""
    def __init__(self, Tipo: Optional["Tipo"], Nome: "Nome"):
        self.Tipo = Tipo
        self.Nome = Nome


class Meionome:
    """Informacao do nome do meio"""
    def __init__(self, Tipo: Optional["Tipo"], Nome: "Nome"):
        self.Tipo = Tipo
        self.Nome = Nome


class Prefixonome:
    """Informacao de prefixo associado a alguma parte do nome (ex: de, da, dos)"""
    def __init__(self, Tipo: Optional["Tipo"], Nome: "Nome"):
        self.Tipo = Tipo
        self.Nome = Nome


class Ultimonome:
    """Informacao do ultimo nome"""
    def __init__(self, Tipo: Optional["Tipo"], Nome: "Nome"):
        self.Tipo = Tipo
        self.Nome = Nome


class Nomepj:
    """Nome de Pessoa Juridica"""
    def __init__(self, tpNome: Optional["Tpnome"], Nome: "Nome"):
        self.tpNome = tpNome
        self.Nome = Nome


class Infonascimento:
    """Demais informacoes de nascimento"""
    def __init__(self, Municipio: Optional["Municipio"], Bairro: Optional["Bairro"], PaisNasc: Optional["Paisnasc"]):
        self.Municipio = Municipio
        self.Bairro = Bairro
        self.PaisNasc = PaisNasc


class Paisnasc:
    """Informacao do pais de nascimento"""
    def __init__(self, Pais: Optional["Pais"], AntigoNomePais: Optional["Antigonomepais"]):
        self.Pais = Pais
        self.AntigoNomePais = AntigoNomePais


class Paisendereco:
    """Pais do endereco principal do declarado"""
    def __init__(self, Pais: "Pais"):
        self.Pais = Pais


class Enderecooutros:
    """Demais enderecos do declarado"""
    def __init__(self, tpEndereco: Optional["Tpendereco"], EnderecoLivre: Optional["Enderecolivre"], EnderecoEstrutura: Optional["Enderecoestrutura"], Pais: "Pais"):
        self.tpEndereco = tpEndereco
        self.EnderecoLivre = EnderecoLivre
        self.EnderecoEstrutura = EnderecoEstrutura
        self.Pais = Pais


class Enderecoestrutura:
    """Endereco na forma estruturada"""
    def __init__(self, EnderecoLivre: Optional["Enderecolivre"], Endereco: Optional["Endereco"], CEP: "Cep", Municipio: "Municipio", UF: "Uf"):
        self.EnderecoLivre = EnderecoLivre
        self.Endereco = Endereco
        self.CEP = CEP
        self.Municipio = Municipio
        self.UF = UF


class Endereco:
    """Dados do endereco na forma estruturada"""
    def __init__(self, Logradouro: Optional["Logradouro"], Numero: Optional["Numero"], Complemento: Optional["Complemento"], Andar: Optional["Andar"], Bairro: Optional["Bairro"], CaixaPostal: Optional["Caixapostal"]):
        self.Logradouro = Logradouro
        self.Numero = Numero
        self.Complemento = Complemento
        self.Andar = Andar
        self.Bairro = Bairro
        self.CaixaPostal = CaixaPostal


class Paisresid:
    """Pais de residencia do declarado"""
    def __init__(self, Pais: "Pais"):
        self.Pais = Pais


class Paisnacionalidade:
    """Pais de nacionalidade do declarado"""
    def __init__(self, Pais: "Pais"):
        self.Pais = Pais


class Proprietarios:
    """Informacoes dos Proprietarios"""
    def __init__(self, tpNI: "Tpni", NIProprietario: "Niproprietario", tpProprietario: Optional["Tpproprietario"], NIF: Optional[List["Nif"]], Nome: "Nome", tpNome: Optional["Tpnome"], NomeOutros: Optional[List["Nomeoutros"]], EnderecoLivre: "Enderecolivre", tpEndereco: Optional["Tpendereco"], PaisEndereco: "Paisendereco", EnderecoOutros: Optional[List["Enderecooutros"]], paisResid: Optional[List["Paisresid"]], PaisNacionalidade: Optional[List["Paisnacionalidade"]], DataNasc: Optional["Datanasc"], InfoNascimento: Optional["Infonascimento"], Reportavel: List["Reportavel"]):
        self.tpNI = tpNI
        self.NIProprietario = NIProprietario
        self.tpProprietario = tpProprietario
        self.NIF = NIF
        self.Nome = Nome
        self.tpNome = tpNome
        self.NomeOutros = NomeOutros
        self.EnderecoLivre = EnderecoLivre
        self.tpEndereco = tpEndereco
        self.PaisEndereco = PaisEndereco
        self.EnderecoOutros = EnderecoOutros
        self.paisResid = paisResid
        self.PaisNacionalidade = PaisNacionalidade
        self.DataNasc = DataNasc
        self.InfoNascimento = InfoNascimento
        self.Reportavel = Reportavel


class Reportavel:
    """Identificacao do(s) pais(es) para o(s) qual(is) o proprietario deve ser reportado"""
    def __init__(self, Pais: "Pais"):
        self.Pais = Pais


class Mescaixa:
    """Operacoes financeiras"""
    def __init__(self, anoMesCaixa: "Anomescaixa", movOpFin: "Movopfin"):
        self.anoMesCaixa = anoMesCaixa
        self.movOpFin = movOpFin


class Movopfin:
    """Operacoes financeiras"""
    def __init__(self, Conta: Optional[List["Conta"]], Cambio: Optional["Cambio"]):
        self.Conta = Conta
        self.Cambio = Cambio


class Conta:
    """Identificacao da conta"""
    def __init__(self, MedJudic: Optional[List["Medjudic"]], infoConta: Optional["Infoconta"]):
        self.MedJudic = MedJudic
        self.infoConta = infoConta


class Medjudic:
    """Identificacao de medidas judiciais"""
    def __init__(self, NumProcJud: "Numprocjud", Vara: "Vara", SecJud: "Secjud", SubSecJud: "Subsecjud", dtConcessao: "Dtconcessao", dtCassacao: Optional["Dtcassacao"]):
        self.NumProcJud = NumProcJud
        self.Vara = Vara
        self.SecJud = SecJud
        self.SubSecJud = SubSecJud
        self.dtConcessao = dtConcessao
        self.dtCassacao = dtCassacao


class Infoconta:
    """Informacoes da conta"""
    def __init__(self, Reportavel: List["Reportavel"], tpConta: "Tpconta", subTpConta: "Subtpconta", tpNumConta: "Tpnumconta", numConta: "Numconta", tpRelacaoDeclarado: "Tprelacaodeclarado", moeda: Optional["Moeda"], Intermediario: Optional["Intermediario"], NoTitulares: Optional["Notitulares"], dtEncerramentoConta: Optional["Dtencerramentoconta"], IndInatividade: Optional["Indinatividade"], IndNDoc: Optional["Indndoc"], Fundo: Optional["Fundo"], BalancoConta: "Balancoconta", PgtosAcum: List["Pgtosacum"]):
        self.Reportavel = Reportavel
        self.tpConta = tpConta
        self.subTpConta = subTpConta
        self.tpNumConta = tpNumConta
        self.numConta = numConta
        self.tpRelacaoDeclarado = tpRelacaoDeclarado
        self.moeda = moeda
        self.Intermediario = Intermediario
        self.NoTitulares = NoTitulares
        self.dtEncerramentoConta = dtEncerramentoConta
        self.IndInatividade = IndInatividade
        self.IndNDoc = IndNDoc
        self.Fundo = Fundo
        self.BalancoConta = BalancoConta
        self.PgtosAcum = PgtosAcum


class Intermediario:
    """Identificacao do intermediario"""
    def __init__(self, GIIN: Optional["Giin"], tpNI: Optional["Tpni"], NIIntermediario: Optional["Niintermediario"]):
        self.GIIN = GIIN
        self.tpNI = tpNI
        self.NIIntermediario = NIIntermediario


class Fundo:
    """Identificacao do fundo"""
    def __init__(self, GIIN: Optional["Giin"], CNPJ: "Cnpj"):
        self.GIIN = GIIN
        self.CNPJ = CNPJ


class Balancoconta:
    """Informacoes de balanco da conta"""
    def __init__(self, totCreditos: "Totcreditos", totDebitos: "Totdebitos", totCreditosMesmaTitularidade: "Totcreditosmesmatitularidade", totDebitosMesmaTitularidade: "Totdebitosmesmatitularidade", vlrUltDia: Optional["Vlrultdia"]):
        self.totCreditos = totCreditos
        self.totDebitos = totDebitos
        self.totCreditosMesmaTitularidade = totCreditosMesmaTitularidade
        self.totDebitosMesmaTitularidade = totDebitosMesmaTitularidade
        self.vlrUltDia = vlrUltDia


class Pgtosacum:
    """Informacoes de pagamentos referentes a conta"""
    def __init__(self, tpPgto: List["Tppgto"], totPgtosAcum: "Totpgtosacum"):
        self.tpPgto = tpPgto
        self.totPgtosAcum = totPgtosAcum


class Cambio:
    """Informacoes sobre operacoes de cambio"""
    def __init__(self, MedJudic: Optional[List["Medjudic"]], totCompras: "Totcompras", totVendas: "Totvendas", totTransferencias: "Tottransferencias"):
        self.MedJudic = MedJudic
        self.totCompras = totCompras
        self.totVendas = totVendas
        self.totTransferencias = totTransferencias


class Signature:
    """"""
    def __init__(self, SignedInfo: "Signedinfo", SignatureValue: "Signaturevalue", KeyInfo: Optional["Keyinfo"], Object: Optional[List["Object"]]):
        self.SignedInfo = SignedInfo
        self.SignatureValue = SignatureValue
        self.KeyInfo = KeyInfo
        self.Object = Object
