from langgraph.pregel.protocol import RunnableConfig

from src.agents.translator_agent import (
    TranslateRequest,
)
from src.graph.config import AppDependencies, GraphConfig
from src.graph.state import CypherTranslation, GraphState


def cypher_generator(state: GraphState, config: RunnableConfig) -> dict:
    """Translate text to cypher."""
    configurable = config.get("configurable", {})
    deps: AppDependencies = configurable["deps"]

    graph_config: GraphConfig = configurable["graph_config"]

    agent = deps.translator_agent

    examples = state.get("retrieved_examples")
    schema = state.get("retrieved_schema")
    entities_record = state.get("entities_record")

    if not examples or not schema or not entities_record:
        raise ValueError("examples or schema not retrieved.")

    allow_entity_discovery = graph_config.allow_entity_discovering

    # if the ontology is not None, then the complete schema has been passed to the LLM. So it can't ask to expand it.
    # if there isn't any new discovered entity, the complete schema has been discovered, so it can't ask to expand it.
    if (
        state["entity_retr_count"] >= graph_config.max_entity_retr_attempts
        or graph_config.ontology_endpoint
        or entities_record.last_added_entities.inner == set()
    ):
        allow_entity_discovery = False

    translate_request = TranslateRequest(
        instruction=state.get("instruction", ""),
        retrieved_examples=examples,
        retrieved_schema=schema,
        attempts=state.get("attempts"),
        lang_syntax=None,
        allow_data_properties_deduction=graph_config.allow_data_properties_deduction,
        allow_entity_discovering=allow_entity_discovery,
    )
    response: CypherTranslation = agent.translate(translate_request)
    response.discover_new_entities = (
        response.discover_new_entities and allow_entity_discovery
    )
    new_count = state.get("try_count", 0)
    # only increment count when the query can pass to the validator node
    if not response.discover_new_entities:
        new_count += 1

    return {"generated_cypher": response, "try_count": new_count}
