from typing import LiteralString, cast

from neo4j import GraphDatabase
from neo4j.exceptions import CypherSyntaxError, CypherTypeError

from src.graph.state import Attempt, AttemptsRecord, GraphState

driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "changeme123"))


def db_validator(state: GraphState) -> dict:
    """Validate genated cypher query in neo4j database and generate the attempt."""
    print("====DB VALIDATOR NODE STATE====")
    print(state)

    last_generated_cypher = state.get("generated_cypher", None)
    if last_generated_cypher is None:
        raise ValueError("Error: generated cypher is None.")

    query = last_generated_cypher.query
    # validate
    validation_query = cast(LiteralString, f"EXPLAIN {query}")

    is_valid = False
    error_message = ""

    with driver.session() as session:
        try:
            session.execute_read(lambda tx: tx.run(validation_query).consume())
            is_valid = True

        except (CypherSyntaxError, CypherSyntaxError, CypherTypeError) as e:
            error_message = f"Errore Neo4j: {e.message}"

            is_valid = False

    attempt: Attempt = cast(
        Attempt, {"generated_cypher": last_generated_cypher, "db_error": error_message}
    )

    attempts_record: AttemptsRecord = state["attempts"]
    attempts_record.attempts.append(attempt)

    state_update = {"is_valid": is_valid, "attempts": attempts_record}
    if is_valid:
        state_update["validated_cypher"] = last_generated_cypher

    return state_update
