from pathlib import Path
from typing import cast

from model.model import model
from src.agents.translator_agent import (
    TranslateRequest,
    TranslatorAgent,
)
from src.graph.state import CypherTranslation, GraphState


def cypher_generator(state: GraphState) -> dict:
    """Translate text to cypher."""
    print("====CYPHER GENERATOR NODE STATE====")
    print(state)

    agent = TranslatorAgent(Path("translator_system_prompt.txt"), model=model)

    translate_request: TranslateRequest = cast(
        TranslateRequest,
        {
            "instruction": state.get("instruction", ""),
            "retrieved_examples": state.get("retrieved_examples", ""),
            "retrieved_schema": state.get("retrieved_schema", ""),
        },
    )

    response: CypherTranslation = agent.translate(translate_request)
    return {"generated_cyper": response}
