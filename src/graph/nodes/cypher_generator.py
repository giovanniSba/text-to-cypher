from agents.agents import get_translator_agent
from src.agents.translator_agent import (
    TranslateRequest,
)
from src.graph.state import CypherTranslation, GraphState


def cypher_generator(state: GraphState) -> dict:
    """Translate text to cypher."""
    print("====CYPHER GENERATOR NODE STATE====")
    print(state)

    agent = get_translator_agent()

    examples = state.get("retrieved_examples")
    schema = state.get("retrieved_schema")

    if not examples or not schema:
        raise ValueError("Error: examples or schema not retrieved.")

    translate_request = TranslateRequest(
        instruction=state.get("instruction", ""),
        retrieved_examples=examples,
        retrieved_schema=schema,
        attempts=state.get("attempts"),
        lang_syntax=None,
    )

    response: CypherTranslation = agent.translate(translate_request)
    return {"generated_cypher": response, "retry_count": state["retry_count"] + 1}
