import json
import xml.etree.ElementTree as ET


def extract_schema_from_owl_to_jsonl(file_path: str, output_path: str):
    """Legge un file OWL/XML ed estrae Nodi, Relazioni e Attributi salvandoli in un file JSONL

    con liste di stringhe per proprietà e relazioni.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()
    ns = {"owl": "http://www.w3.org/2002/07/owl#"}

    # --- ESTRAZIONE CLASSI ---
    classes = set()
    for decl in root.findall("owl:Declaration", ns):
        cls = decl.find("owl:Class", ns)
        if cls is not None:
            iri = cls.get("IRI") or cls.get("abbreviatedIRI")
            if iri:
                classes.add(iri.split("/")[-1])

    # Inizializza i dizionari per raggruppare i dati per ogni classe come liste di stringhe
    attributes_by_class = {c: [] for c in classes}
    relations_by_class = {c: [] for c in classes}

    # --- ESTRAZIONE OBJECT PROPERTIES (Relazioni) ---
    obj_domains = {}
    obj_ranges = {}

    for dom in root.findall("owl:ObjectPropertyDomain", ns):
        prop = dom.find("owl:ObjectProperty", ns)
        cls = dom.find("owl:Class", ns)
        if prop is not None and cls is not None:
            obj_domains[prop.get("IRI").split("/")[-1]] = cls.get("IRI").split("/")[-1]

    for rng in root.findall("owl:ObjectPropertyRange", ns):
        prop = rng.find("owl:ObjectProperty", ns)
        cls = rng.find("owl:Class", ns)
        if prop is not None and cls is not None:
            obj_ranges[prop.get("IRI").split("/")[-1]] = cls.get("IRI").split("/")[-1]

    # Popola le relazioni nel formato richiesto: entità-relazione->entità
    for prop_name, domain_class in obj_domains.items():
        if domain_class in relations_by_class and prop_name in obj_ranges:
            range_class = obj_ranges[prop_name]
            relations_by_class[domain_class].append(
                f"{domain_class} {prop_name} {range_class}"
            )

    # --- ESTRAZIONE DATA PROPERTIES (Attributi / Proprietà) ---
    data_domains = {}
    data_ranges = {}

    for dom in root.findall("owl:DataPropertyDomain", ns):
        prop = dom.find("owl:DataProperty", ns)
        cls = dom.find("owl:Class", ns)
        if prop is not None and cls is not None:
            data_domains[prop.get("IRI").split("/")[-1]] = cls.get("IRI").split("/")[-1]

    for rng in root.findall("owl:DataPropertyRange", ns):
        prop = rng.find("owl:DataProperty", ns)
        dt = rng.find("owl:Datatype", ns)
        if prop is not None and dt is not None:
            # Pulisce 'xsd:string' in 'string'
            dt_type = (
                dt.get("abbreviatedIRI").replace("xsd:", "")
                if dt.get("abbreviatedIRI")
                else "string"
            )
            data_ranges[prop.get("IRI").split("/")[-1]] = dt_type

    # Popola le proprietà nel formato richiesto: entità-proprietà->tipo
    for prop_name, class_name in data_domains.items():
        if class_name in attributes_by_class:
            dt_type = data_ranges.get(prop_name, "string")
            attributes_by_class[class_name].append(f"{prop_name}: {dt_type}")

    # --- SALVATAGGIO IN JSONL ---
    with open(output_path, "w", encoding="utf-8") as f:
        for cls in sorted(classes):
            entity_data = {
                "entity": cls,
                "properties": attributes_by_class[
                    cls
                ],  # Ora è una lista di stringhe ["Persona-nome->string"]
                "relations": relations_by_class[
                    cls
                ],  # È una lista di stringhe ["Persona-lavoraIn->Azienda"]
            }
            f.write(json.dumps(entity_data) + "\n")

    print(f"Salvataggio completato! Dati esportati in: {output_path}")


# Esecuzione
extract_schema_from_owl_to_jsonl("maestro.owl", "schema_output.jsonl")
