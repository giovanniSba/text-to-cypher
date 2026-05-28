from src.agent.state import AgentState


def cypher_generator(state: AgentState) -> AgentState:
    """Translate text to cypher."""
    state["generated_cyper"] = "match (c:Clients) return c"
    return state
