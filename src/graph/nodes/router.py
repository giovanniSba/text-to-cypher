from langgraph.constants import END

from src.graph.state import GraphState

MAX_ATTEMPTS = 3


def validator_router(state: GraphState) -> str:
    """Router after db validation."""
    if state.get("final_error") is not None:
        return "error_handler"
    elif state["is_valid"]:
        return END
    elif state["retry_count"] >= MAX_ATTEMPTS:
        return "error_handler"
    else:
        return "cypher_generator"


def global_router(state: GraphState, next_node: str) -> str:
    """Manage cenetralize error handling."""
    if state.get("final_error") is not None:
        return "error_handler"
    return next_node
