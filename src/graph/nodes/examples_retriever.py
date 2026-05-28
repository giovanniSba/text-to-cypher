from src.graph.state import AgentState


def examples_retriever(state: AgentState) -> dict:
    """Extract correct entities from DB schema."""
    return {
        "retrieved_examples": [("Mostrami tutti i film", "match (f: Film) return f")]
    }
