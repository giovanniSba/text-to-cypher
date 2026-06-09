import requests
from langgraph.pregel.protocol import RunnableConfig

from graph.config import GraphConfig
from src.graph.state import DBSchema, GraphState
from utils.owl_utils import parse_owl_to_entities


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

    if graph_config.enable_owl_parsing:
        schema = DBSchema(db_schema=parse_owl_to_entities(response.text))
    else:
        schema = response.text
    return {"retrieved_schema": schema}
