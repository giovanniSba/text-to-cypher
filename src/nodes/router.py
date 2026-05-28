from langgraph.graph import END

from src.agent.state import AgentState

MAX_ATTEMPS = 3


def validator_router(state: AgentState) -> str:
    """Router after db validation."""
    if state["is_valid"] or state["retry_count"] >= MAX_ATTEMPS:
        return END
    else:
        return "cypher_generator"
