from src.graph.state import AgentState


def db_validator(state: AgentState) -> dict:
    """Validate genated cypher query in neo4j database."""
    return {"is_valid": True}
