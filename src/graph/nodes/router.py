from langgraph.pregel.protocol import RunnableConfig

from src.graph.config import GraphConfig
from src.graph.state import GraphState


def validator_router(state: GraphState, config: RunnableConfig) -> str:
    """Router after db validation."""
    configurable = config.get("configurable", {})
    graph_config: GraphConfig = configurable["graph_config"]

    if state["try_count"] >= graph_config.max_gen_attempts or state["is_valid"]:
        next = "output_formatter"
    else:
        next = "cypher_generator"

    return global_router(state, next)


def schema_router(state: GraphState, config: RunnableConfig) -> str:
    """Router for entity retrieve/ontology fetching."""
    configurable = config.get("configurable", {})
    graph_config: GraphConfig = configurable["graph_config"]

    if graph_config.ontology_endpoint is None:
        next = "entity_retriever"
    else:
        next = "external_schema_fetcher"
    return global_router(state, next)


def cypher_generation_router(state: GraphState, config: RunnableConfig) -> str:
    """Router for generation/entity_retriever node."""
    configurable = config.get("configurable", {})
    graph_config: GraphConfig = configurable["graph_config"]

    entity_retr_count = state.get("entity_retr_count", 0)

    generated_cypher = state.get("generated_cypher")
    if generated_cypher is None:
        raise ValueError("Generated cypher is none")

    if (
        entity_retr_count >= graph_config.max_entity_retr_attempts
        or not generated_cypher.discover_new_entities
    ):
        next = "db_validator"
    else:
        next = "entity_retriever"
    return global_router(state, next)


def global_router(state: GraphState, next_node: str) -> str:
    """Manage cenetralize error handling."""
    if state.get("final_error") is not None:
        return "error_handler"
    return next_node
