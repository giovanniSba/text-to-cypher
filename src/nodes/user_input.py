from src.agent.state import AgentState


def user_input(state: AgentState) -> AgentState:
    """Get the user's instruction prompt."""
    instruction: str = "Show me all clients"
    state["instruction"] = instruction

    return state
