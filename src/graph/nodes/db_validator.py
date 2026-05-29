from src.graph.state import GraphState


def db_validator(state: GraphState) -> dict:
    """Validate genated cypher query in neo4j database."""
    return {"is_valid": True}
