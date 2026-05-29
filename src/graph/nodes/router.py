from langgraph.graph import END

from src.graph.state import GraphState

MAX_ATTEMPS = 3


def validator_router(state: GraphState) -> str:
    """Router after db validation."""
    if state["is_valid"] or state["retry_count"] >= MAX_ATTEMPS:
        return END
    else:
        return "cypher_generator"
