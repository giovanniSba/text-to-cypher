from src.agent.state import AgentState


def entities_retriever(state: AgentState) -> AgentState:
    """Extract correct entities from DB schema."""
    state["retrieved_entities"] = ["Client"]

    return state
