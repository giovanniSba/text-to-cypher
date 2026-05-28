from dataclasses import dataclass
from typing import Any, TypedDict


@dataclass
class AgentState(TypedDict):
    """Input state for the agent."""

    instruction: str  # user input
    generated_cyper: str  # translated query
    retrieved_entities: list[Any]  # entities structure TBD
    retrieved_examples: list[Any]  # example structure TBD
    db_error_msg: str
    is_valid: bool
    retry_count: int
