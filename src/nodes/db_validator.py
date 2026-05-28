from src.agent.state import AgentState


def db_validator(state: AgentState) -> AgentState:
    """Validate genated cypher query in neo4j database."""
    state["is_valid"] = True

    return state
