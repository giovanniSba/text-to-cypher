from langgraph.pregel.protocol import RunnableConfig

from graph.nodes.db_validator import db_validator
from src.graph.config import GraphConfig
from src.graph.state import CypherTranslation, GraphState


def validator_router(state: GraphState, config: RunnableConfig) -> str:
    """Router after db validation."""
    configurable = config.get("configurable", {})
    graph_config: GraphConfig = configurable["graph_config"]

    if state.get("final_error") is not None:
        return "error_handler"
    elif state["try_count"] > graph_config.max_gen_attempts or state["is_valid"]:
        return "output_formatter"
    else:
        return "cypher_generator"


def schema_router(state: GraphState, config: RunnableConfig) -> str:
    """Router for entity retrieve/ontology fetching."""
    configurable = config.get("configurable", {})
    graph_config: GraphConfig = configurable["graph_config"]

    if graph_config.ontology_endpoint is None:
        return "entity_retriever"
    else:
        return "external_schema_fetcher"


max_gen_ent = 0


def cypher_generation_router(state: GraphState) -> str:
    """Router for generation/entity_retriever node."""
    if state.get("final_error") is not None:
        return "error_handler"

    generated_cypher = state.get("generated_cypher")
    if generated_cypher is None:
        raise ValueError("Generated cypher is none")

    global max_gen_ent
    if max_gen_ent > 3:
        return "db_validator"

    if generated_cypher.discover_new_entities:
        max_gen_ent += 1
        return "entity_retriever"
    else:
        return "db_validator"


def global_router(state: GraphState, next_node: str) -> str:
    """Manage cenetralize error handling."""
    if state.get("final_error") is not None:
        return "error_handler"
    return next_node
