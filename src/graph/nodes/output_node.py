from graph.state import GraphState


def output_formatter(state: GraphState) -> dict:
    """Fill empty field of the final state."""
    config = state.get("config_params")
    last_attempt = state["attempts"].attempts[-1]

    try_count = state.get("try_count", 0)
    if try_count > config.max_gen_attempts:
        try_count = config.max_gen_attempts

    state_update = {}
    if last_attempt:
        state_update = {
            "final_warnings": last_attempt.db_warnings,
            "final_error": last_attempt.db_error,
            "final_note": last_attempt.generated_cypher.note,
            "try_count": try_count,
        }

    return state_update
