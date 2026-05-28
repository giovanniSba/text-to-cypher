from src.graph.state import AgentState


def entities_retriever(state: AgentState) -> dict:
    """Extract correct entities from DB schema."""
    return {"retrieved_entities": ["Client"]}
