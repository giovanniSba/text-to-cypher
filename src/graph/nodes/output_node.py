from graph.nodes.router import MAX_ATTEMPTS
from graph.state import GraphState


def output_formatter(state: GraphState) -> dict:
    """Fill empty field of the final state."""
    last_attempt = state["attempts"].attempts.pop()

    try_count = state.get("try_count", 0)
    if try_count > MAX_ATTEMPTS:
        try_count = MAX_ATTEMPTS

    state_update = {}
    if last_attempt:
        state_update = {
            "final_warnings": last_attempt.db_warnings,
            "final_error": last_attempt.db_error,
            "final_note": last_attempt.generated_cypher.note,
            "try_count": try_count,
        }

    return state_update
