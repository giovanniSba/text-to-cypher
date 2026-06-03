from typing import TypedDict, cast

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


class Attempt(BaseModel):
    generated_cypher: CypherTranslation = Field(
        description="Query cypher generata per instruction"
    )
    db_error: str = Field(description="Errore generato dalla validazione su database")


class AttemptsRecord(BaseModel):
    instruction: str = Field(description="Testo naturale da convertire in query cypher")
    attempts: list[Attempt] = Field(
        description="Tentativi di traduzione eseguiti per instruction"
    )


class GraphState(TypedDict):
    """Input state for the agent."""

    instruction: str  # user input
    generated_cypher: CypherTranslation | None  # translated query
    validated_cypher: CypherTranslation | None
    final_error: str | None
    retrieved_entities: Entities | None
    retrieved_examples: Examples | None
    retrieved_schema: DBSchema | None
    attempts: AttemptsRecord
    is_valid: bool | None
    retry_count: int


def create_init_state(instruction: str) -> GraphState:
    """Return the init state."""
    attempts = AttemptsRecord(instruction=instruction, attempts=[])
    init_state = {"instruction": instruction, "retry_count": 0, "attempts": attempts}

    return cast(GraphState, init_state)
