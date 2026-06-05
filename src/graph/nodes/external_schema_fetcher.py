import os

import requests

from src.graph.state import DBSchema, GraphState
from utils.owl_utils import parse_owl_to_entities

ENABLE_OWL_PARSING = os.environ.get("ENABLE_OWL_PARSING", "False").lower() in (
    "true",
    "1",
    "t",
)


def external_schema_fetcher(state: GraphState) -> dict:
    """Fetch the full schema from an external OWL endpoint."""
    endpoint = state.get("ontology_endpoint")

    if endpoint is None:
        raise ValueError("Endpoint not found.")

    # http request
    response = requests.get(endpoint, headers={"accept": "application/json"})
    response.raise_for_status()

    if ENABLE_OWL_PARSING:
        schema = DBSchema(db_schema=parse_owl_to_entities(response.text))
    else:
        schema = response.text
    return {"retrieved_schema": schema}
