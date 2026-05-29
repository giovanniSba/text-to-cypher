from src.graph.state import GraphState


def examples_retriever(state: GraphState) -> dict:
    """Extract correct entities from DB schema."""
    return {
        "retrieved_examples": [("Mostrami tutti i film", "match (f: Film) return f")]
    }
