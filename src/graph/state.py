from dataclasses import dataclass
from typing import Any, TypedDict, cast

from pydantic import BaseModel, Field


class QueryExample(BaseModel):
    instruction: str
    expected: str


class Examples(BaseModel):
    examples: list[QueryExample] = Field(
        description="Una lista di esempi simili alla richiesta dell'utente"
    )


class Entities(BaseModel):
    entities: list[str] = Field(
        description="Una lista di entità rilevanti estratte dal testo"
    )


class DBEntity(BaseModel):
    name: str = Field(description="Nome dell'entità")
    properties: list[str] = Field(description="Proprietà dell'entità")
    relations: list[str] = Field(
        description="Relazioni dell'entità con le altre entità dello schema"
    )


class DBSchema(BaseModel):
    db_schema: list[DBEntity] = Field(
        description="Schema del database espresso come lista di entità, proprietà e relazioni fra esse"
    )


class CypherTranslation(BaseModel):
    query: str = Field(
        description="La query Cypher finale generata, senza markdown o testo aggiuntivo"
    )
    error: str = Field(
        description="Descrizione di un eventuale errore incontrato durante il processo di traduzione"
    )


@dataclass
class GraphState(TypedDict):
    """Input state for the agent."""

    instruction: str  # user input
    generated_cyper: CypherTranslation  # translated query
    retrieved_entities: Entities
    retrieved_examples: Examples
    retrieved_schema: DBSchema
    db_error_msg: str
    is_valid: bool
    retry_count: int


def create_init_state(instruction: str) -> GraphState:
    """Return the init state."""
    init_state = {"instruction": instruction, "retry_count": 0}

    return cast(GraphState, init_state)
