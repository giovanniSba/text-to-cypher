from typing import LiteralString, cast

from neo4j.exceptions import CypherSyntaxError, CypherTypeError, Neo4jError

from src.graph.state import Attempt, AttemptsRecord, GraphState
from utils.neo4j import get_driver


def db_validator(state: GraphState) -> dict:
    """Validate genated cypher query in neo4j database and generate the attempt."""
    attempts_record: AttemptsRecord = state["attempts"]
    driver = get_driver()

    last_generated_cypher = state.get("generated_cypher", None)
    if last_generated_cypher is None:
        raise ValueError("generated cypher is None.")

    if last_generated_cypher.query is None:
        raise ValueError(last_generated_cypher.error)
    query = last_generated_cypher.query.strip()
    # validate
    validation_query = cast(LiteralString, f"EXPLAIN {query}")

    is_valid = False
    error_message = ""

    with driver.session() as session:
        try:
            session.execute_read(lambda tx: tx.run(validation_query).consume())
            is_valid = True

        except (CypherSyntaxError, CypherTypeError, Neo4jError) as e:
            error_message = e.message
            is_valid = False

    attempt: Attempt = cast(
        Attempt, {"generated_cypher": last_generated_cypher, "db_error": error_message}
    )

    attempts_record.attempts.append(attempt)

    # if an error occurred to the last generated query, make another attempt anyway
    if last_generated_cypher.error is not None:
        is_valid = False
    state_update = {"is_valid": is_valid, "attempts": attempts_record}
    if is_valid:
        state_update["validated_cypher"] = last_generated_cypher

    return state_update
