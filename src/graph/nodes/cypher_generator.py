from typing import cast

from src.agents.translator_agent import (
    TranslateRequest,
    TranslatorAgent,
)
from src.graph.state import GraphState


def cypher_generator(state: GraphState) -> dict:
    """Translate text to cypher."""
    agent = TranslatorAgent()

    translate_request: TranslateRequest = cast(
        TranslateRequest,
        {
            "instruction": state.get("instruction", ""),
            "retrieved_examples": state.get("retrieved_examples", ""),
            "retrieved_entities": state.get("retrieved_entities", ""),
        },
    )

    response = agent.translate(translate_request)
    cypher_query = response.content[0].get("text", "Error in query translation")
    print(cypher_query)
    return {"generated_cyper": cypher_query}
