from src.agent.state import AgentState


def examples_retriever(state: AgentState) -> AgentState:
    """Extract correct entities from DB schema."""
    state["retrieved_examples"] = [
        ("Mostrami tutti i film", "match (f: Film) return f")
    ]

    return state
