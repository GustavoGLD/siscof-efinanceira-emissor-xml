import xmlschema
from lxml import etree as ET
from pathlib import Path
import uuid

# Função para converter nome qualificado para nome com prefixo
def get_prefixed_name(qname: str, nsmap: dict) -> str:
    if "}" in qname:
        ns, local_name = qname.split("}")
        ns = ns[1:]  # Remove '{'
        for prefix, uri in nsmap.items():
            if uri == ns:
                return f"{prefix}:{local_name}" if prefix else local_name
    return qname

# Função para criar um elemento XSD com namespace
def create_xsd_element(tag, nsmap=None, **attribs):
    if nsmap is None:
        nsmap = {
            'xs': 'http://www.w3.org/2001/XMLSchema',
            # None: 'http://www.eFinanceira.gov.br/schemas/evtMovOpFin/v1_2_1',
            'ds': 'http://www.w3.org/2000/09/xmldsig#'
        }
    qname = ET.QName('http://www.w3.org/2001/XMLSchema', tag)
    elem = ET.Element(qname, attrib=attribs, nsmap=nsmap)
    return elem

# Função para converter um componente XSD (xmlschema) em lxml.etree
def convert_component_to_etree(component, parent, nsmap):
    if isinstance(component, xmlschema.validators.XsdElement):
        elem = create_xsd_element('element', nsmap, name=component.local_name)
        if component.min_occurs != 1:
            elem.set('minOccurs', str(component.min_occurs))
        if component.max_occurs != 1:
            elem.set('maxOccurs', 'unbounded' if component.max_occurs is None else str(component.max_occurs))
        if component.annotation and component.annotation.documentation:
            annotation = create_xsd_element('annotation', nsmap)
            for doc in (component.annotation.documentation if isinstance(component.annotation.documentation, list) else [component.annotation.documentation]):
                if doc.text:
                    doc_elem = create_xsd_element('documentation', nsmap)
                    doc_elem.text = doc.text
                    annotation.append(doc_elem)
            elem.append(annotation)
        if component.type:
            if component.type.name:
                elem.set('type', component.type.name)
            else:
                # Tipo anônimo
                type_elem = create_xsd_element('complexType' if isinstance(component.type, xmlschema.validators.XsdComplexType) else 'simpleType', nsmap)
                convert_type_to_etree(component.type, type_elem, nsmap)
                elem.append(type_elem)
        parent.append(elem)
    elif isinstance(component, xmlschema.validators.XsdAttribute):
        attr = create_xsd_element('attribute', nsmap, name=component.local_name)
        if component.use == 'required':
            attr.set('use', 'required')
        if component.type.name:
            attr.set('type', get_prefixed_name(component.type.name, nsmap))
        if component.annotation and component.annotation.documentation:
            annotation = create_xsd_element('annotation', nsmap)
            for doc in (component.annotation.documentation if isinstance(component.annotation.documentation, list) else [component.annotation.documentation]):
                if doc.text:
                    doc_elem = create_xsd_element('documentation', nsmap)
                    doc_elem.text = doc.text
                    annotation.append(doc_elem)
            attr.append(annotation)
        parent.append(attr)

# Função para converter um tipo XSD em lxml.etree
def convert_type_to_etree(type_obj, parent, nsmap):
    if isinstance(type_obj, xmlschema.validators.XsdComplexType):
        if type_obj.content:
            sequence = create_xsd_element('sequence', nsmap)
            for child in type_obj.content.iter_elements():
                convert_component_to_etree(child, sequence, nsmap)
            parent.append(sequence)
        for attr_name, attr in type_obj.attributes.items():
            convert_component_to_etree(attr, parent, nsmap)
    elif isinstance(type_obj, xmlschema.validators.XsdSimpleType):
        restriction = create_xsd_element('restriction', nsmap, base=get_prefixed_name(type_obj.base_type.name, nsmap))
        for facet_name, facet in type_obj.facets.items():
            if facet_name == 'minLength':
                restriction.append(create_xsd_element('minLength', nsmap, value=str(facet.value)))
            elif facet_name == 'maxLength':
                restriction.append(create_xsd_element('maxLength', nsmap, value=str(facet.value)))
            elif facet_name == 'pattern':
                restriction.append(create_xsd_element('pattern', nsmap, value=facet.pattern))
        parent.append(restriction)

# Função principal para gerar XSDs
def generate_xsd_files():
    schema_path = r"C:\Users\lidio\PycharmProjects\siscof-efinanceira-emissor-xml\schemas\evtFechamentoeFinanceira-v1_3_0.xsd"
    schema = xmlschema.XMLSchema(schema_path)
    output_dir = Path("schemas/subschemas/fechamento")
    output_dir.mkdir(exist_ok=True)

    processed = set()

    # Iterar sobre todos os elementos e seus componentes
    for sch in schema.elements.values():
        for elem in sch.iter_components():
            if isinstance(elem, xmlschema.validators.XsdElement) and isinstance(elem.type, xmlschema.validators.XsdComplexType):
                name = elem.local_name
                if name in processed or elem.name == '{http://www.w3.org/2000/09/xmldsig#}Signature':
                    continue
                processed.add(name)

                # Criar um novo documento XSD
                nsmap = {
                    'xs': 'http://www.w3.org/2001/XMLSchema',
                    #None: 'http://www.eFinanceira.gov.br/schemas/evtMovOpFin/v1_2_1',
                    'ds': 'http://www.w3.org/2000/09/xmldsig#'
                }
                schema_elem = create_xsd_element('schema', nsmap,
                    elementFormDefault='qualified',
                    attributeFormDefault='unqualified',
                    #targetNamespace='http://www.eFinanceira.gov.br/schemas/evtMovOpFin/v1_2_1'
                )

                # Adicionar import para xmldsig se necessário
                if 'ds:Signature' in str(elem):
                    import_elem = create_xsd_element('import', nsmap,
                        namespace='http://www.w3.org/2000/09/xmldsig#',
                        schemaLocation='../../Comum/xmldsig-core-schema.xsd'
                    )
                    schema_elem.append(import_elem)

                # Criar elemento raiz para o complexType
                root_elem = create_xsd_element('element', nsmap, name=name)
                if elem.annotation and elem.annotation.documentation:
                    annotation = create_xsd_element('annotation', nsmap)
                    for doc in (elem.annotation.documentation if isinstance(elem.annotation.documentation, list) else [elem.annotation.documentation]):
                        if doc.text:
                            doc_elem = create_xsd_element('documentation', nsmap)
                            doc_elem.text = doc.text
                            annotation.append(doc_elem)
                    root_elem.append(annotation)

                # Adicionar o complexType
                complex_type = create_xsd_element('complexType', nsmap)
                convert_type_to_etree(elem.type, complex_type, nsmap)
                root_elem.append(complex_type)
                schema_elem.append(root_elem)

                # Salvar o arquivo XSD
                tree = ET.ElementTree(schema_elem)
                output_path = output_dir / f"{name}.xsd"
                tree.write(output_path, encoding='utf-8', xml_declaration=True, pretty_print=True)

if __name__ == "__main__":
    generate_xsd_files()