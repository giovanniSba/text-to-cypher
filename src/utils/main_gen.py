import json
import logging
import xml.etree.ElementTree as ET
from typing import Dict, List

# Assumo che _extract_suffix, DBEntity e logger siano importati o definiti altrove
logger = logging.getLogger(__name__)


def _extract_suffix(element: ET.Element | None) -> str:
    if element is None:
        return ""
    iri = element.get("IRI") or element.get("abbreviatedIRI") or ""
    return iri.split("/")[-1]


def parse_owl_file_to_jsonl(input_filepath: str, output_jsonl_path: str):
    """Parse un file OWL, salva il risultato in .jsonl e ritorna la lista di DBEntity."""
    ns = {"owl": "http://www.w3.org/2002/07/owl#"}

    # 1. Legge direttamente dal file invece che dalla stringa
    tree = ET.parse(input_filepath)
    root = tree.getroot()

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
            fmt_domain = domain_class
            fmt_range = range_class
            relations[domain_class].append(f"{fmt_domain} {prop_name} {fmt_range}")

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
            attributes[class_name].append(f"{prop_name}: {dt_type}")

    # 2. Final assembly & Salvataggio in JSONL

    with open(output_jsonl_path, "w", encoding="utf-8") as f:
        for cls in sorted(classes):
            # Serializzazione manuale in dizionario per evitare errori con json.dumps.
            # Nota: se DBEntity usa Pydantic puoi usare `entity.model_dump()`,
            # se è una dataclass puoi usare `dataclasses.asdict(entity)`.
            entity_dict = {
                "entity": cls,
                "properties": attributes[cls],
                "relations": relations[cls],
            }

            # Scrive l'oggetto JSON su una nuova riga (formato JSONL)
            f.write(json.dumps(entity_dict, ensure_ascii=False) + "\n")

    logger.info(f"Parsing completato: entità in {output_jsonl_path}")


parse_owl_file_to_jsonl("maestro.owl", "schema_output_v2.jsonl")
