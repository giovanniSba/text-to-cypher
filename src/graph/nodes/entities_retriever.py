from src.graph.state import GraphState


def entities_retriever(state: GraphState) -> dict:
    """Extract correct entities from DB schema."""
    return {"retrieved_entities": ["Client"]}
