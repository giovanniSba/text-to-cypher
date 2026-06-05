from typing import LiteralString, cast

from neo4j import NotificationSeverity
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
    error_message = None
    warnings: list[str] | None = None

    with driver.session() as session:
        try:
            result = session.execute_read(lambda tx: tx.run(validation_query).consume())

            # retrieve generated warnings
            for stat in result.gql_status_objects:
                if stat.severity == NotificationSeverity.WARNING:
                    warnings = warnings or []
                    warnings.append(stat.status_description)

            is_valid = True

        except (CypherSyntaxError, CypherTypeError, Neo4jError) as e:
            error_message = e.message
            is_valid = False

    attempt = Attempt(
        generated_cypher=last_generated_cypher,
        db_error=error_message,
        db_warnings=warnings,
    )

    attempts_record.attempts.append(attempt)

    # if an error occurred to the last generated query, make another attempt anyway
    if last_generated_cypher.error is not None:
        is_valid = False

    if warnings is not None:
        is_valid = False

    state_update = {"is_valid": is_valid, "attempts": attempts_record}

    return state_update
