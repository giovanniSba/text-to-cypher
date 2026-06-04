import json
import logging
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def _extract_suffix(element: ET.Element | None) -> str:
    """Safely extract the IRI suffix."""
    if element is None:
        return ""
    iri = element.get("IRI") or element.get("abbreviatedIRI") or ""
    return iri.split("/")[-1]


def _format_pascal(text: str) -> str:
    """Format string to Pascal_Case."""
    return text.replace("_", " ").title().replace(" ", "_")


def _format_camel(text: str) -> str:
    """Format string to camelCase."""
    if not text:
        return ""
    title_case = text.title().replace("_", "")
    return title_case[0].lower() + title_case[1:]


def parse_owl_to_jsonl(input_file: str | Path, output_file: str | Path) -> None:
    """Parse OWL/XML and export schema mapping to JSONL."""
    ns = {"owl": "http://www.w3.org/2002/07/owl#"}
    in_path, out_path = Path(input_file), Path(output_file)

    if not in_path.is_file():
        logging.error(f"Input file not found: {in_path}")
        return

    tree = ET.parse(in_path)
    root = tree.getroot()

    # Extract classes
    classes = {
        _extract_suffix(decl.find("owl:Class", ns))
        for decl in root.findall("owl:Declaration", ns)
    }
    classes.discard("")

    attributes: Dict[str, List[str]] = {c: [] for c in classes}
    relations: Dict[str, List[str]] = {c: [] for c in classes}

    # Extract object properties (Relations)
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

    # Extract data properties (Attributes)
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

    # Export to JSONL
    with out_path.open("w", encoding="utf-8") as f:
        for cls in sorted(classes):
            record = {
                "entity": cls,
                "properties": attributes[cls],
                "relations": relations[cls],
            }
            f.write(json.dumps(record) + "\n")
    logging.info(f"Successfully exported schema to: {out_path}")


parse_owl_to_jsonl("maestro.owl", "schema_output.jsonl")
