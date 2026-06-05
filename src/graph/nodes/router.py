from src.graph.state import GraphState


def validator_router(state: GraphState) -> str:
    """Router after db validation."""
    config = state.get("config_params")
    if state.get("final_error") is not None:
        return "error_handler"
    elif state["try_count"] > config.max_gen_attempts or state["is_valid"]:
        return "output_formatter"
    else:
        return "cypher_generator"


def schema_router(state: GraphState) -> str:
    """Router for entity retrieve/ontology fetching."""
    config = state.get("config_params")
    if config.ontology_endpoint is None:
        return "entity_retriever"
    else:
        return "external_schema_fetcher"


def global_router(state: GraphState, next_node: str) -> str:
    """Manage cenetralize error handling."""
    if state.get("final_error") is not None:
        return "error_handler"
    return next_node
