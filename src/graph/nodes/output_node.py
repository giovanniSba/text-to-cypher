from langgraph.pregel.protocol import RunnableConfig

from graph.config import GraphConfig
from graph.state import GraphState


def output_formatter(state: GraphState, config: RunnableConfig) -> dict:
    """Fill empty field of the final state."""
    configurable = config.get("configurable", {})
    graph_config: GraphConfig = configurable["graph_config"]

    last_attempt = state["attempts"].attempts[-1]

    try_count = state.get("try_count", 0)
    if try_count > graph_config.max_gen_attempts:
        try_count = graph_config.max_gen_attempts

    state_update = {}
    if last_attempt:
        state_update = {
            "final_warnings": last_attempt.db_warnings,
            "final_error": last_attempt.db_error,
            "final_note": last_attempt.generated_cypher.note,
            "try_count": try_count,
        }

    return state_update
