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

    if not examples or not schema:
        raise ValueError("examples or schema not retrieved.")

    translate_request = TranslateRequest(
        instruction=state.get("instruction", ""),
        retrieved_examples=examples,
        retrieved_schema=schema,
        attempts=state.get("attempts"),
        lang_syntax=None,
        allow_data_properties_deduction=graph_config.allow_data_properties_deduction,
    )

    response: CypherTranslation = agent.translate(translate_request)

    # if the ontology is not None, then the complete schema has been passed to the LLM. So it can't ask to expand it.
    if graph_config.ontology_endpoint:
        response.discover_new_entities = False

    new_count = state.get("try_count", 0)
    # only increment count when the query can pass to the validator node
    if not response.discover_new_entities:
        new_count += 1

    return {"generated_cypher": response, "try_count": new_count}
