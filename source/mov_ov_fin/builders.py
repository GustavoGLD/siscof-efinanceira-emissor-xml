import os
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.dom import minidom

from lxml import etree as LET


from .types import *
from typing import Dict, Optional
from abc import ABC, abstractmethod

class XmlBuilderInterface(ABC):
    @abstractmethod
    def build(self, obj) -> ET.Element: ...

class XmlAdapter:
    @staticmethod
    def create_element(tag: str, text: Optional[str]=None, attrib: Optional[Dict[str,str]]=None)->ET.Element:
        el=ET.Element(tag, attrib=attrib or {})
        if text is not None: el.text=text
        return el

    @staticmethod
    def append_child(parent: ET.Element, tag:str, text:Optional[str]=None, attrib:Optional[Dict[str,str]]=None)->ET.Element:
        ch=XmlAdapter.create_element(tag,text,attrib)
        parent.append(ch)
        return ch


class EvtmovopfinXmlBuilder(XmlBuilderInterface):
    def build(self, obj: Evtmovopfin) -> ET.Element:
        root = XmlAdapter.create_element(
            "eFinanceira",
            attrib={
                "xmlns": "http://www.eFinanceira.gov.br/schemas/evtMovOpFin/v1_2_1"
            }
        )

        el = XmlAdapter.create_element("evtMovOpFin")
        el.set("id", str(obj.id))

        el.append(IdeeventoXmlBuilder().build(obj.ideEvento))
        el.append(IdedeclaranteXmlBuilder().build(obj.ideDeclarante))
        el.append(IdedeclaradoXmlBuilder().build(obj.ideDeclarado))
        el.append(MescaixaXmlBuilder().build(obj.mesCaixa))

        root.append(el)

        xml_str = ET.tostring(root, encoding="utf-8")
        #print(minidom.parseString(xml_str).toprettyxml(indent="  "))

        with open(f"{(Path(__file__).resolve().parent.parent.parent)}\\schemas\\evtMovOpFin-v1_2_1.xsd", "rb") as f:
            schema_doc = LET.parse(f)
        schema = LET.XMLSchema(schema_doc)

        # Valida XML
        doc = LET.fromstring(xml_str)
        if not schema.validate(doc):
            raise ValueError(f"\n{str(schema.error_log)}\nXML:\n{xml_str}")
        return root


class IdeeventoXmlBuilder(XmlBuilderInterface):
    def build(self, obj: Ideevento) -> ET.Element:
        el = XmlAdapter.create_element("ideEvento")
        XmlAdapter.append_child(el, 'indRetificacao', str(obj.indRetificacao))
        if obj.nrRecibo: XmlAdapter.append_child(el, 'nrRecibo', str(obj.nrRecibo))
        XmlAdapter.append_child(el, 'tpAmb', str(obj.tpAmb))
        XmlAdapter.append_child(el, 'aplicEmi', str(obj.aplicEmi))
        XmlAdapter.append_child(el, 'verAplic', str(obj.verAplic))
        return el


class IdedeclaranteXmlBuilder(XmlBuilderInterface):
    def build(self, obj: Idedeclarante) -> ET.Element:
        el = XmlAdapter.create_element("ideDeclarante")
        XmlAdapter.append_child(el, 'cnpjDeclarante', str(obj.cnpjDeclarante))
        return el


class IdedeclaradoXmlBuilder(XmlBuilderInterface):
    def build(self, obj: Idedeclarado) -> ET.Element:
        el = XmlAdapter.create_element("ideDeclarado")
        XmlAdapter.append_child(el, 'tpNI', str(obj.tpNI))
        if obj.tpDeclarado:
            for item in obj.tpDeclarado:
                XmlAdapter.append_child(el, 'tpDeclarado', str(item))
        XmlAdapter.append_child(el, 'NIDeclarado', str(obj.NIDeclarado))
        if obj.NIF:
            for item in obj.NIF:
                el.append(NifXmlBuilder().build(item))
        XmlAdapter.append_child(el, 'NomeDeclarado', str(obj.NomeDeclarado))
        if obj.tpNomeDeclarado: XmlAdapter.append_child(el, 'tpNomeDeclarado', str(obj.tpNomeDeclarado))
        if obj.NomeOutros:
            for item in obj.NomeOutros:
                el.append(NomeoutrosXmlBuilder().build(item))
        if obj.DataNasc: XmlAdapter.append_child(el, 'DataNasc', str(obj.DataNasc))
        if obj.InfoNascimento: el.append(InfonascimentoXmlBuilder().build(obj.InfoNascimento))
        if obj.EnderecoLivre: XmlAdapter.append_child(el, 'EnderecoLivre', str(obj.EnderecoLivre))
        if obj.tpEndereco: XmlAdapter.append_child(el, 'tpEndereco', str(obj.tpEndereco))
        el.append(PaisenderecoXmlBuilder().build(obj.PaisEndereco))
        if obj.EnderecoOutros:
            for item in obj.EnderecoOutros:
                el.append(EnderecooutrosXmlBuilder().build(item))
        if obj.paisResid:
            for item in obj.paisResid:
                el.append(PaisresidXmlBuilder().build(item))
        if obj.PaisNacionalidade:
            for item in obj.PaisNacionalidade:
                el.append(PaisnacionalidadeXmlBuilder().build(item))
        if obj.Proprietarios:
            for item in obj.Proprietarios:
                el.append(ProprietariosXmlBuilder().build(item))
        return el


class NifXmlBuilder(XmlBuilderInterface):
    def build(self, obj: Nif) -> ET.Element:
        el = XmlAdapter.create_element("NIF")
        XmlAdapter.append_child(el, 'NumeroNIF', str(obj.NumeroNIF))
        XmlAdapter.append_child(el, 'PaisEmissaoNIF', str(obj.PaisEmissaoNIF))
        if obj.tpNIF: XmlAdapter.append_child(el, 'tpNIF', str(obj.tpNIF))
        return el


class NomeoutrosXmlBuilder(XmlBuilderInterface):
    def build(self, obj: Nomeoutros) -> ET.Element:
        el = XmlAdapter.create_element("NomeOutros")
        if obj.NomePF: el.append(NomepfXmlBuilder().build(obj.NomePF))
        if obj.NomePJ: el.append(NomepjXmlBuilder().build(obj.NomePJ))
        return el


class NomepfXmlBuilder(XmlBuilderInterface):
    def build(self, obj: Nomepf) -> ET.Element:
        el = XmlAdapter.create_element("NomePF")
        if obj.tpNome: XmlAdapter.append_child(el, 'tpNome', str(obj.tpNome))
        if obj.PrecTitulo: XmlAdapter.append_child(el, 'PrecTitulo', str(obj.PrecTitulo))
        if obj.Titulo:
            for item in obj.Titulo:
                XmlAdapter.append_child(el, 'Titulo', str(item))
        el.append(PrimeironomeXmlBuilder().build(obj.PrimeiroNome))
        if obj.MeioNome:
            for item in obj.MeioNome:
                el.append(MeionomeXmlBuilder().build(item))
        if obj.PrefixoNome: el.append(PrefixonomeXmlBuilder().build(obj.PrefixoNome))
        el.append(UltimonomeXmlBuilder().build(obj.UltimoNome))
        if obj.IdGeracao:
            for item in obj.IdGeracao:
                XmlAdapter.append_child(el, 'IdGeracao', str(item))
        if obj.Sufixo:
            for item in obj.Sufixo:
                XmlAdapter.append_child(el, 'Sufixo', str(item))
        if obj.GenSufixo: XmlAdapter.append_child(el, 'GenSufixo', str(obj.GenSufixo))
        return el


class PrimeironomeXmlBuilder(XmlBuilderInterface):
    def build(self, obj: Primeironome) -> ET.Element:
        el = XmlAdapter.create_element("PrimeiroNome")
        if obj.Tipo: XmlAdapter.append_child(el, 'Tipo', str(obj.Tipo))
        XmlAdapter.append_child(el, 'Nome', str(obj.Nome))
        return el


class MeionomeXmlBuilder(XmlBuilderInterface):
    def build(self, obj: Meionome) -> ET.Element:
        el = XmlAdapter.create_element("MeioNome")
        if obj.Tipo: XmlAdapter.append_child(el, 'Tipo', str(obj.Tipo))
        XmlAdapter.append_child(el, 'Nome', str(obj.Nome))
        return el


class PrefixonomeXmlBuilder(XmlBuilderInterface):
    def build(self, obj: Prefixonome) -> ET.Element:
        el = XmlAdapter.create_element("PrefixoNome")
        if obj.Tipo: XmlAdapter.append_child(el, 'Tipo', str(obj.Tipo))
        XmlAdapter.append_child(el, 'Nome', str(obj.Nome))
        return el


class UltimonomeXmlBuilder(XmlBuilderInterface):
    def build(self, obj: Ultimonome) -> ET.Element:
        el = XmlAdapter.create_element("UltimoNome")
        if obj.Tipo: XmlAdapter.append_child(el, 'Tipo', str(obj.Tipo))
        XmlAdapter.append_child(el, 'Nome', str(obj.Nome))
        return el


class NomepjXmlBuilder(XmlBuilderInterface):
    def build(self, obj: Nomepj) -> ET.Element:
        el = XmlAdapter.create_element("NomePJ")
        if obj.tpNome: XmlAdapter.append_child(el, 'tpNome', str(obj.tpNome))
        XmlAdapter.append_child(el, 'Nome', str(obj.Nome))
        return el


class InfonascimentoXmlBuilder(XmlBuilderInterface):
    def build(self, obj: Infonascimento) -> ET.Element:
        el = XmlAdapter.create_element("InfoNascimento")
        if obj.Municipio: XmlAdapter.append_child(el, 'Municipio', str(obj.Municipio))
        if obj.Bairro: XmlAdapter.append_child(el, 'Bairro', str(obj.Bairro))
        if obj.PaisNasc: el.append(PaisnascXmlBuilder().build(obj.PaisNasc))
        return el


class PaisnascXmlBuilder(XmlBuilderInterface):
    def build(self, obj: Paisnasc) -> ET.Element:
        el = XmlAdapter.create_element("PaisNasc")
        if obj.Pais: XmlAdapter.append_child(el, 'Pais', str(obj.Pais))
        if obj.AntigoNomePais: XmlAdapter.append_child(el, 'AntigoNomePais', str(obj.AntigoNomePais))
        return el


class PaisenderecoXmlBuilder(XmlBuilderInterface):
    def build(self, obj: Paisendereco) -> ET.Element:
        el = XmlAdapter.create_element("PaisEndereco")
        XmlAdapter.append_child(el, 'Pais', str(obj.Pais))
        return el


class EnderecooutrosXmlBuilder(XmlBuilderInterface):
    def build(self, obj: Enderecooutros) -> ET.Element:
        el = XmlAdapter.create_element("EnderecoOutros")
        if obj.tpEndereco: XmlAdapter.append_child(el, 'tpEndereco', str(obj.tpEndereco))
        if obj.EnderecoLivre: XmlAdapter.append_child(el, 'EnderecoLivre', str(obj.EnderecoLivre))
        if obj.EnderecoEstrutura: el.append(EnderecoestruturaXmlBuilder().build(obj.EnderecoEstrutura))
        XmlAdapter.append_child(el, 'Pais', str(obj.Pais))
        return el


class EnderecoestruturaXmlBuilder(XmlBuilderInterface):
    def build(self, obj: Enderecoestrutura) -> ET.Element:
        el = XmlAdapter.create_element("EnderecoEstrutura")
        if obj.EnderecoLivre: XmlAdapter.append_child(el, 'EnderecoLivre', str(obj.EnderecoLivre))
        if obj.Endereco: el.append(EnderecoXmlBuilder().build(obj.Endereco))
        XmlAdapter.append_child(el, 'CEP', str(obj.CEP))
        XmlAdapter.append_child(el, 'Municipio', str(obj.Municipio))
        XmlAdapter.append_child(el, 'UF', str(obj.UF))
        return el


class EnderecoXmlBuilder(XmlBuilderInterface):
    def build(self, obj: Endereco) -> ET.Element:
        el = XmlAdapter.create_element("Endereco")
        if obj.Logradouro: XmlAdapter.append_child(el, 'Logradouro', str(obj.Logradouro))
        if obj.Numero: XmlAdapter.append_child(el, 'Numero', str(obj.Numero))
        if obj.Complemento: XmlAdapter.append_child(el, 'Complemento', str(obj.Complemento))
        if obj.Andar: XmlAdapter.append_child(el, 'Andar', str(obj.Andar))
        if obj.Bairro: XmlAdapter.append_child(el, 'Bairro', str(obj.Bairro))
        if obj.CaixaPostal: XmlAdapter.append_child(el, 'CaixaPostal', str(obj.CaixaPostal))
        return el


class PaisresidXmlBuilder(XmlBuilderInterface):
    def build(self, obj: Paisresid) -> ET.Element:
        el = XmlAdapter.create_element("paisResid")
        XmlAdapter.append_child(el, 'Pais', str(obj.Pais))
        return el


class PaisnacionalidadeXmlBuilder(XmlBuilderInterface):
    def build(self, obj: Paisnacionalidade) -> ET.Element:
        el = XmlAdapter.create_element("PaisNacionalidade")
        XmlAdapter.append_child(el, 'Pais', str(obj.Pais))
        return el


class ProprietariosXmlBuilder(XmlBuilderInterface):
    def build(self, obj: Proprietarios) -> ET.Element:
        el = XmlAdapter.create_element("Proprietarios")
        XmlAdapter.append_child(el, 'tpNI', str(obj.tpNI))
        XmlAdapter.append_child(el, 'NIProprietario', str(obj.NIProprietario))
        if obj.tpProprietario: XmlAdapter.append_child(el, 'tpProprietario', str(obj.tpProprietario))
        if obj.NIF:
            for item in obj.NIF:
                el.append(NifXmlBuilder().build(item))
        XmlAdapter.append_child(el, 'Nome', str(obj.Nome))
        if obj.tpNome: XmlAdapter.append_child(el, 'tpNome', str(obj.tpNome))
        if obj.NomeOutros:
            for item in obj.NomeOutros:
                el.append(NomeoutrosXmlBuilder().build(item))
        XmlAdapter.append_child(el, 'EnderecoLivre', str(obj.EnderecoLivre))
        if obj.tpEndereco: XmlAdapter.append_child(el, 'tpEndereco', str(obj.tpEndereco))
        el.append(PaisenderecoXmlBuilder().build(obj.PaisEndereco))
        if obj.EnderecoOutros:
            for item in obj.EnderecoOutros:
                el.append(EnderecooutrosXmlBuilder().build(item))
        if obj.paisResid:
            for item in obj.paisResid:
                el.append(PaisresidXmlBuilder().build(item))
        if obj.PaisNacionalidade:
            for item in obj.PaisNacionalidade:
                el.append(PaisnacionalidadeXmlBuilder().build(item))
        if obj.DataNasc: XmlAdapter.append_child(el, 'DataNasc', str(obj.DataNasc))
        if obj.InfoNascimento: el.append(InfonascimentoXmlBuilder().build(obj.InfoNascimento))
        if obj.Reportavel:
            for item in obj.Reportavel:
                el.append(ReportavelXmlBuilder().build(item))
        return el


class ReportavelXmlBuilder(XmlBuilderInterface):
    def build(self, obj: Reportavel) -> ET.Element:
        el = XmlAdapter.create_element("Reportavel")
        XmlAdapter.append_child(el, 'Pais', str(obj.Pais))
        return el


class MescaixaXmlBuilder(XmlBuilderInterface):
    def build(self, obj: Mescaixa) -> ET.Element:
        el = XmlAdapter.create_element("mesCaixa")
        XmlAdapter.append_child(el, 'anoMesCaixa', str(obj.anoMesCaixa))
        el.append(MovopfinXmlBuilder().build(obj.movOpFin))
        return el


class MovopfinXmlBuilder(XmlBuilderInterface):
    def build(self, obj: Movopfin) -> ET.Element:
        el = XmlAdapter.create_element("movOpFin")
        if obj.Conta:
            for item in obj.Conta:
                el.append(ContaXmlBuilder().build(item))
        if obj.Cambio: el.append(CambioXmlBuilder().build(obj.Cambio))
        return el


class ContaXmlBuilder(XmlBuilderInterface):
    def build(self, obj: Conta) -> ET.Element:
        el = XmlAdapter.create_element("Conta")
        if obj.MedJudic:
            for item in obj.MedJudic:
                el.append(MedjudicXmlBuilder().build(item))
        if obj.infoConta: el.append(InfocontaXmlBuilder().build(obj.infoConta))
        return el


class MedjudicXmlBuilder(XmlBuilderInterface):
    def build(self, obj: Medjudic) -> ET.Element:
        el = XmlAdapter.create_element("MedJudic")
        XmlAdapter.append_child(el, 'NumProcJud', str(obj.NumProcJud))
        XmlAdapter.append_child(el, 'Vara', str(obj.Vara))
        XmlAdapter.append_child(el, 'SecJud', str(obj.SecJud))
        XmlAdapter.append_child(el, 'SubSecJud', str(obj.SubSecJud))
        XmlAdapter.append_child(el, 'dtConcessao', str(obj.dtConcessao))
        if obj.dtCassacao: XmlAdapter.append_child(el, 'dtCassacao', str(obj.dtCassacao))
        return el


class InfocontaXmlBuilder(XmlBuilderInterface):
    def build(self, obj: Infoconta) -> ET.Element:
        el = XmlAdapter.create_element("infoConta")
        if obj.Reportavel:
            for item in obj.Reportavel:
                el.append(ReportavelXmlBuilder().build(item))
        XmlAdapter.append_child(el, 'tpConta', str(obj.tpConta))
        XmlAdapter.append_child(el, 'subTpConta', str(obj.subTpConta))
        XmlAdapter.append_child(el, 'tpNumConta', str(obj.tpNumConta))
        XmlAdapter.append_child(el, 'numConta', str(obj.numConta))
        XmlAdapter.append_child(el, 'tpRelacaoDeclarado', str(obj.tpRelacaoDeclarado))
        if obj.moeda: XmlAdapter.append_child(el, 'moeda', str(obj.moeda))
        if obj.Intermediario: el.append(IntermediarioXmlBuilder().build(obj.Intermediario))
        if obj.NoTitulares: XmlAdapter.append_child(el, 'NoTitulares', str(obj.NoTitulares))
        if obj.dtEncerramentoConta: XmlAdapter.append_child(el, 'dtEncerramentoConta', str(obj.dtEncerramentoConta))
        if obj.IndInatividade: XmlAdapter.append_child(el, 'IndInatividade', str(obj.IndInatividade))
        if obj.IndNDoc: XmlAdapter.append_child(el, 'IndNDoc', str(obj.IndNDoc))
        if obj.Fundo: el.append(FundoXmlBuilder().build(obj.Fundo))
        el.append(BalancocontaXmlBuilder().build(obj.BalancoConta))
        if obj.PgtosAcum:
            for item in obj.PgtosAcum:
                el.append(PgtosacumXmlBuilder().build(item))
        return el


class IntermediarioXmlBuilder(XmlBuilderInterface):
    def build(self, obj: Intermediario) -> ET.Element:
        el = XmlAdapter.create_element("Intermediario")
        if obj.GIIN: XmlAdapter.append_child(el, 'GIIN', str(obj.GIIN))
        if obj.tpNI: XmlAdapter.append_child(el, 'tpNI', str(obj.tpNI))
        if obj.NIIntermediario: XmlAdapter.append_child(el, 'NIIntermediario', str(obj.NIIntermediario))
        return el


class FundoXmlBuilder(XmlBuilderInterface):
    def build(self, obj: Fundo) -> ET.Element:
        el = XmlAdapter.create_element("Fundo")
        if obj.GIIN: XmlAdapter.append_child(el, 'GIIN', str(obj.GIIN))
        XmlAdapter.append_child(el, 'CNPJ', str(obj.CNPJ))
        return el


class BalancocontaXmlBuilder(XmlBuilderInterface):
    def build(self, obj: Balancoconta) -> ET.Element:
        el = XmlAdapter.create_element("BalancoConta")
        XmlAdapter.append_child(el, 'totCreditos', str(obj.totCreditos))
        XmlAdapter.append_child(el, 'totDebitos', str(obj.totDebitos))
        XmlAdapter.append_child(el, 'totCreditosMesmaTitularidade', str(obj.totCreditosMesmaTitularidade))
        XmlAdapter.append_child(el, 'totDebitosMesmaTitularidade', str(obj.totDebitosMesmaTitularidade))
        if obj.vlrUltDia: XmlAdapter.append_child(el, 'vlrUltDia', str(obj.vlrUltDia))
        return el


class PgtosacumXmlBuilder(XmlBuilderInterface):
    def build(self, obj: Pgtosacum) -> ET.Element:
        el = XmlAdapter.create_element("PgtosAcum")
        if obj.tpPgto:
            for item in obj.tpPgto:
                XmlAdapter.append_child(el, 'tpPgto', str(item))
        XmlAdapter.append_child(el, 'totPgtosAcum', str(obj.totPgtosAcum))
        return el


class CambioXmlBuilder(XmlBuilderInterface):
    def build(self, obj: Cambio) -> ET.Element:
        el = XmlAdapter.create_element("Cambio")
        if obj.MedJudic:
            for item in obj.MedJudic:
                el.append(MedjudicXmlBuilder().build(item))
        XmlAdapter.append_child(el, 'totCompras', str(obj.totCompras))
        XmlAdapter.append_child(el, 'totVendas', str(obj.totVendas))
        XmlAdapter.append_child(el, 'totTransferencias', str(obj.totTransferencias))
        return el
