import xml.etree.ElementTree as ET
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


class EvtfechamentoefinanceiraXmlBuilder(XmlBuilderInterface):
    def build(self, obj: Evtfechamentoefinanceira) -> ET.Element:
        el = XmlAdapter.create_element("evtFechamentoeFinanceira")
        el.set('id', str(obj.id))
        el.append(IdeeventoXmlBuilder().build(obj.ideEvento))
        el.append(IdedeclaranteXmlBuilder().build(obj.ideDeclarante))
        el.append(InfofechamentoXmlBuilder().build(obj.infoFechamento))
        if obj.FechamentoPP: el.append(FechamentoppXmlBuilder().build(obj.FechamentoPP))
        if obj.FechamentoMovOpFin: el.append(FechamentomovopfinXmlBuilder().build(obj.FechamentoMovOpFin))
        if obj.FechamentoMovOpFinAnual: el.append(FechamentomovopfinanualXmlBuilder().build(obj.FechamentoMovOpFinAnual))
        return el


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


class InfofechamentoXmlBuilder(XmlBuilderInterface):
    def build(self, obj: Infofechamento) -> ET.Element:
        el = XmlAdapter.create_element("infoFechamento")
        XmlAdapter.append_child(el, 'dtInicio', str(obj.dtInicio))
        XmlAdapter.append_child(el, 'dtFim', str(obj.dtFim))
        XmlAdapter.append_child(el, 'sitEspecial', str(obj.sitEspecial))
        if obj.nadaADeclarar: XmlAdapter.append_child(el, 'nadaADeclarar', str(obj.nadaADeclarar))
        return el


class FechamentoppXmlBuilder(XmlBuilderInterface):
    def build(self, obj: Fechamentopp) -> ET.Element:
        el = XmlAdapter.create_element("FechamentoPP")
        XmlAdapter.append_child(el, 'FechamentoPP', str(obj.FechamentoPP))
        return el


class FechamentomovopfinXmlBuilder(XmlBuilderInterface):
    def build(self, obj: Fechamentomovopfin) -> ET.Element:
        el = XmlAdapter.create_element("FechamentoMovOpFin")
        XmlAdapter.append_child(el, 'FechamentoMovOpFin', str(obj.FechamentoMovOpFin))
        if obj.EntDecExterior: el.append(EntdecexteriorXmlBuilder().build(obj.EntDecExterior))
        if obj.EntPatDecExterior:
            for item in obj.EntPatDecExterior:
                el.append(EntpatdecexteriorXmlBuilder().build(item))
        return el


class EntdecexteriorXmlBuilder(XmlBuilderInterface):
    def build(self, obj: Entdecexterior) -> ET.Element:
        el = XmlAdapter.create_element("EntDecExterior")
        XmlAdapter.append_child(el, 'ContasAReportar', str(obj.ContasAReportar))
        return el


class EntpatdecexteriorXmlBuilder(XmlBuilderInterface):
    def build(self, obj: Entpatdecexterior) -> ET.Element:
        el = XmlAdapter.create_element("EntPatDecExterior")
        XmlAdapter.append_child(el, 'GIIN', str(obj.GIIN))
        XmlAdapter.append_child(el, 'CNPJ', str(obj.CNPJ))
        if obj.ContasAReportar: XmlAdapter.append_child(el, 'ContasAReportar', str(obj.ContasAReportar))
        if obj.inCadPatrocinadoEncerrado: XmlAdapter.append_child(el, 'inCadPatrocinadoEncerrado', str(obj.inCadPatrocinadoEncerrado))
        if obj.inGIINEncerrado: XmlAdapter.append_child(el, 'inGIINEncerrado', str(obj.inGIINEncerrado))
        return el


class FechamentomovopfinanualXmlBuilder(XmlBuilderInterface):
    def build(self, obj: Fechamentomovopfinanual) -> ET.Element:
        el = XmlAdapter.create_element("FechamentoMovOpFinAnual")
        XmlAdapter.append_child(el, 'FechamentoMovOpFinAnual', str(obj.FechamentoMovOpFinAnual))
        return el


