import xml.etree.ElementTree as ET
from typing import Dict, List

from loguru import logger

from src.graph.state import DBEntity


# helpers
def _extract_suffix(element: ET.Element | None) -> str:
    if element is None:
        return ""
    iri = element.get("IRI") or element.get("abbreviatedIRI") or ""
    return iri.split("/")[-1]


def _format_pascal(text: str) -> str:
    return text.replace("_", " ").title().replace(" ", "_")


def _format_camel(text: str) -> str:
    if not text:
        return ""
    title_case = text.title().replace("_", "")
    return title_case[0].lower() + title_case[1:]


def parse_owl_to_entities(owl_string: str) -> list[DBEntity]:
    """Parse owl to list[DBEntity]."""
    ns = {"owl": "http://www.w3.org/2002/07/owl#"}
    root = ET.fromstring(owl_string)

    # init & classes
    classes = {
        _extract_suffix(decl.find("owl:Class", ns))
        for decl in root.findall("owl:Declaration", ns)
    }
    classes.discard("")

    attributes: Dict[str, List[str]] = {c: [] for c in classes}
    relations: Dict[str, List[str]] = {c: [] for c in classes}

    # object properties
    obj_domains = {
        _extract_suffix(dom.find("owl:ObjectProperty", ns)): _extract_suffix(
            dom.find("owl:Class", ns)
        )
        for dom in root.findall("owl:ObjectPropertyDomain", ns)
    }

    obj_ranges = {
        _extract_suffix(rng.find("owl:ObjectProperty", ns)): _extract_suffix(
            rng.find("owl:Class", ns)
        )
        for rng in root.findall("owl:ObjectPropertyRange", ns)
    }

    for prop_name, domain_class in obj_domains.items():
        range_class = obj_ranges.get(prop_name)
        if prop_name and domain_class in relations and range_class:
            fmt_domain = _format_pascal(domain_class)
            fmt_range = _format_pascal(range_class)
            relations[domain_class].append(
                f"{fmt_domain} {prop_name.upper()} {fmt_range}"
            )

    # data properties
    data_domains = {
        _extract_suffix(dom.find("owl:DataProperty", ns)): _extract_suffix(
            dom.find("owl:Class", ns)
        )
        for dom in root.findall("owl:DataPropertyDomain", ns)
    }

    data_ranges = {}
    for rng in root.findall("owl:DataPropertyRange", ns):
        prop_name = _extract_suffix(rng.find("owl:DataProperty", ns))
        dt = rng.find("owl:Datatype", ns)
        if prop_name and dt is not None:
            abbr = dt.get("abbreviatedIRI", "")
            data_ranges[prop_name] = abbr.replace("xsd:", "") if abbr else "string"

    for prop_name, class_name in data_domains.items():
        if prop_name and class_name in attributes:
            dt_type = data_ranges.get(prop_name, "string")
            attributes[class_name].append(f"{_format_camel(prop_name)}: {dt_type}")

    # final assembly
    entities = []
    for cls in sorted(classes):
        entities.append(
            DBEntity(
                name=cls,
                properties=attributes[cls],
                relations=relations[cls],
            )
        )

    logger.info("Parsing owl ontology to list[DBEntity] completed")
    return entities


# parse_owl_to_jsonl("maestro.owl", "schema_output.jsonl")
