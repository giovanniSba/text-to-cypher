import xml.etree.ElementTree as ET


def extract_schema_from_owl(file_path: str) -> str:
    """Legge un file OWL/XML ed estrae Nodi, Relazioni e Attributi per il prompt LLM."""
    tree = ET.parse(file_path)
    root = tree.getroot()
    ns = {"owl": "http://www.w3.org/2002/07/owl#"}

    classes = set()
    for decl in root.findall("owl:Declaration", ns):
        cls = decl.find("owl:Class", ns)
        if cls is not None:
            iri = cls.get("IRI") or cls.get("abbreviatedIRI")
            if iri:
                classes.add(iri.split("/")[-1])

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

    relations = []
    for prop_name, domain_class in obj_domains.items():
        if prop_name in obj_ranges:
            range_class = obj_ranges[prop_name]
            relations.append(f"- {domain_class} -> {prop_name} -> {range_class}")

    # --- ESTRAZIONE DATA PROPERTIES (Attributi) ---
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

    # Mappa gli attributi alle rispettive classi
    attributes_by_class = {c: [] for c in classes}
    for prop_name, class_name in data_domains.items():
        if class_name in attributes_by_class:
            dt_type = data_ranges.get(prop_name, "string")
            attributes_by_class[class_name].append(f"{prop_name} ({dt_type})")

    # --- COSTRUZIONE OUTPUT ---
    schema_text = "CLASSI VALIDE E LORO ATTRIBUTI:\n"
    for cls in sorted(classes):
        attrs = (
            ", ".join(attributes_by_class[cls])
            if attributes_by_class[cls]
            else "Nessun attributo"
        )
        schema_text += f"- {cls}: [{attrs}]\n"

    schema_text += "\nRELAZIONI VALIDE (Dominio -> Relazione -> Range):\n" + "\n".join(
        relations
    )

    return schema_text


result = extract_schema_from_owl("maestro.owl")
print(result)
