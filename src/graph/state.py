from dataclasses import dataclass
from typing import Any, TypedDict, cast


@dataclass
class GraphState(TypedDict):
    """Input state for the agent."""

    instruction: str  # user input
    generated_cyper: str  # translated query
    retrieved_entities: list[Any]  # entities structure TBD
    retrieved_examples: list[Any]  # example structure TBD
    db_error_msg: str
    is_valid: bool
    retry_count: int


def create_init_state(instruction: str) -> GraphState:
    """Return the init state."""
    init_state = {"instruction": instruction, "retry_count": 0}

    return cast(GraphState, init_state)
