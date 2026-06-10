from socket import inet_ntoa
from typing import cast

import pyoxigraph
import requests
from langgraph.pregel.protocol import RunnableConfig

from graph.config import GraphConfig
from src.graph.state import DBSchema, GraphState
from utils.owl_utils import parse_owl_to_entities


class OntologyLoader:
    def __init__(self):
        self._store = pyoxigraph.Store()

    def load_ontology(self, content: str, format_type: str):
        match format_type:
            case "rdf":
                rdf_format = pyoxigraph.RdfFormat.RDF_XML
            case _:
                raise ValueError("Ontology format not allowed.")

        self._store.load(content, rdf_format)

    def get_schema_relations(self) -> dict:
        def _clean_uri(uri: str) -> str:
            if not uri:
                return ""
            return uri.split("#")[-1].split("/")[-1].lstrip("/")

        schema = {}

        # --- 1. QUERY PER LE OBJECT PROPERTIES (RELAZIONI) ---
        query_relations = """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>

        SELECT DISTINCT ?sourceClass ?relation ?targetClass
        WHERE {
            ?relation a owl:ObjectProperty .
            ?relation rdfs:domain ?sourceClass .
            ?relation rdfs:range ?targetClass .
        }
        """
        # Nota: per i SELECT il tipo corretto in pyoxigraph è QuerySolutions
        results_rel = cast(
            pyoxigraph.QuerySolutions, self._store.query(query_relations)
        )

        for solution in results_rel:
            source = _clean_uri(solution["sourceClass"].value)
            relation = _clean_uri(
                solution["relation"].value
            ).upper()  # Convenzione Neo4j (es. TREATS)
            target = _clean_uri(solution["targetClass"].value)

            if source not in schema:
                schema[source] = {"data_properties": [], "relations": []}

            schema[source]["relations"].append({"relation": relation, "target": target})

        # --- 2. QUERY PER LE DATATYPE PROPERTIES (ATTRIBUTI) ---
        query_properties = """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>

        SELECT DISTINCT ?class ?property ?type
        WHERE {
            ?property a owl:DatatypeProperty .
            ?property rdfs:domain ?class .
            OPTIONAL { ?property rdfs:range ?type }
        }
        """
        results_prop = cast(
            pyoxigraph.QuerySolutions, self._store.query(query_properties)
        )

        for solution in results_prop:
            source = _clean_uri(solution["class"].value)
            prop_name = _clean_uri(solution["property"].value)

            # Gestione del tipo (se l'OPTIONAL è vuoto, la chiave non è nella soluzione)
            dt_type = "STRING"
            if "type" in solution and solution["type"] is not None:
                raw_type = _clean_uri(solution["type"].value).upper()
                if "INT" in raw_type or "INTEGER" in raw_type:
                    dt_type = "INT"
                elif "BOOLEAN" in raw_type:
                    dt_type = "BOOLEAN"
                elif "FLOAT" in raw_type or "DOUBLE" in raw_type:
                    dt_type = "FLOAT"

            if source not in schema:
                schema[source] = {"data_properties": [], "relations": []}

            schema[source]["data_properties"].append(
                {"name": prop_name, "type": dt_type}
            )

        return schema


def external_schema_fetcher(state: GraphState, config: RunnableConfig) -> dict:
    """Fetch the full schema from an external OWL endpoint."""
    configurable = config.get("configurable", {})
    graph_config: GraphConfig = configurable["graph_config"]

    endpoint = graph_config.ontology_endpoint

    if endpoint is None:
        raise ValueError("Endpoint not found.")

    # http request
    response = requests.get(str(endpoint), headers={"accept": "application/json"})
    response.raise_for_status()

    print(response.text)

    ont_loader = OntologyLoader()
    ont_loader.load_ontology(response.text, "rdf")

    parsed = ont_loader.get_schema_relations()

    print(f"SCHEMA RELATIONS: {parsed}")
    return {"retrieved_schema": DBSchema()}
