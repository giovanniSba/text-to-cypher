import os

from src.graph.state import GraphState

MAX_ATTEMPTS = int(os.environ.get("MAX_ATTEMPTS", "3"))


def validator_router(state: GraphState) -> str:
    """Router after db validation."""
    if state.get("final_error") is not None:
        return "error_handler"
    elif state["try_count"] > MAX_ATTEMPTS or state["is_valid"]:
        return "output_formatter"
    else:
        return "cypher_generator"


def schema_router(state: GraphState) -> str:
    """Router for entity retrieve/ontology fetching."""
    ontology_endpoint = state.get("ontology_endpoint")
    if ontology_endpoint is None:
        return "entity_retriever"
    else:
        return "external_schema_fetcher"


def global_router(state: GraphState, next_node: str) -> str:
    """Manage cenetralize error handling."""
    if state.get("final_error") is not None:
        return "error_handler"
    return next_node
