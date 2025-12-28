import re
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


class Dtinicio:
    """Data Inicial no formato AAAA-MM-DD"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Dtinicio":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Dtfim:
    """Data Final no formato AAAA-MM-DD"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Dtfim":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Sitespecial:
    """Indicador de Situacao Especial 0 - Nao se aplica 1 - Extincao 2 - Fusao 3 - Incorporacao/Incorporada 5 - Cisao Total"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Sitespecial":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Nadaadeclarar:
    """Indicador de nada a declarar no periodo: 1 - nada a declarar no periodo"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Nadaadeclarar":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Contasareportar:
    """"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Contasareportar":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Giin:
    """GIIN"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Giin":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Cnpj:
    """CNPJ"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Cnpj":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Incadpatrocinadoencerrado:
    """O fundo foi encerrado e nao serao enviadas contas para este fundo"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Incadpatrocinadoencerrado":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Ingiinencerrado:
    """O GIIN foi encerrado no IRS"""
    def __init__(self, value: str):
        pass
        self.value = value

    @classmethod
    def from_str(cls, val: str) -> "Ingiinencerrado":
        return cls(val)

    def __str__(self):
        return str(self.value)


class Efinanceira:
    """"""
    def __init__(self, evtFechamentoeFinanceira: "Evtfechamentoefinanceira", Signature: "Signature"):
        self.evtFechamentoeFinanceira = evtFechamentoeFinanceira
        self.Signature = Signature


class Evtfechamentoefinanceira:
    """Evento de Fechamento da eFinanceira"""
    def __init__(self, id: str, ideEvento: "Ideevento", ideDeclarante: "Idedeclarante", infoFechamento: "Infofechamento", FechamentoPP: Optional["Fechamentopp"], FechamentoMovOpFin: Optional["Fechamentomovopfin"], FechamentoMovOpFinAnual: Optional["Fechamentomovopfinanual"]):
        self.id = id
        self.ideEvento = ideEvento
        self.ideDeclarante = ideDeclarante
        self.infoFechamento = infoFechamento
        self.FechamentoPP = FechamentoPP
        self.FechamentoMovOpFin = FechamentoMovOpFin
        self.FechamentoMovOpFinAnual = FechamentoMovOpFinAnual


class Ideevento:
    """Informacoes de identificacao do evento"""
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


class Infofechamento:
    """"""
    def __init__(self, dtInicio: "Dtinicio", dtFim: "Dtfim", sitEspecial: "Sitespecial", nadaADeclarar: Optional["Nadaadeclarar"]):
        self.dtInicio = dtInicio
        self.dtFim = dtFim
        self.sitEspecial = sitEspecial
        self.nadaADeclarar = nadaADeclarar


class Fechamentopp:
    """"""
    def __init__(self, FechamentoPP: "Fechamentopp"):
        self.FechamentoPP = FechamentoPP


class Fechamentomovopfin:
    """"""
    def __init__(self, FechamentoMovOpFin: "Fechamentomovopfin", EntDecExterior: Optional["Entdecexterior"], EntPatDecExterior: Optional[List["Entpatdecexterior"]]):
        self.FechamentoMovOpFin = FechamentoMovOpFin
        self.EntDecExterior = EntDecExterior
        self.EntPatDecExterior = EntPatDecExterior


class Entdecexterior:
    """"""
    def __init__(self, ContasAReportar: "Contasareportar"):
        self.ContasAReportar = ContasAReportar


class Entpatdecexterior:
    """"""
    def __init__(self, GIIN: "Giin", CNPJ: "Cnpj", ContasAReportar: Optional["Contasareportar"], inCadPatrocinadoEncerrado: Optional["Incadpatrocinadoencerrado"], inGIINEncerrado: Optional["Ingiinencerrado"]):
        self.GIIN = GIIN
        self.CNPJ = CNPJ
        self.ContasAReportar = ContasAReportar
        self.inCadPatrocinadoEncerrado = inCadPatrocinadoEncerrado
        self.inGIINEncerrado = inGIINEncerrado


class Fechamentomovopfinanual:
    """"""
    def __init__(self, FechamentoMovOpFinAnual: "Fechamentomovopfinanual"):
        self.FechamentoMovOpFinAnual = FechamentoMovOpFinAnual


class Signature:
    """"""
    def __init__(self, SignedInfo: "Signedinfo", SignatureValue: "Signaturevalue", KeyInfo: Optional["Keyinfo"], Object: Optional[List["Object"]]):
        self.SignedInfo = SignedInfo
        self.SignatureValue = SignatureValue
        self.KeyInfo = KeyInfo
        self.Object = Object
