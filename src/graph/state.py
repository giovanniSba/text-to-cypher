from typing import TypedDict, cast

from pydantic import BaseModel, Field


class QueryExample(BaseModel):
    """NL-Cypher pair."""

    instruction: str
    expected: str


class Examples(BaseModel):
    """Example list."""

    examples: list[QueryExample] = Field(
        description="Una lista di esempi simili alla richiesta dell'utente"
    )


class Entities(BaseModel):
    """List of entities involved."""

    entities: list[str] = Field(
        description="Una lista di entità rilevanti estratte dal testo"
    )


class DBEntity(BaseModel):
    """Representation of entities in the database."""

    name: str = Field(description="Nome dell'entità")
    properties: list[str] = Field(description="Proprietà dell'entità")
    relations: list[str] = Field(
        description="Relazioni dell'entità con le altre entità dello schema"
    )


class DBSchema(BaseModel):
    """List of DBEntity that represent the DB schema."""

    db_schema: list[DBEntity] = Field(
        description="Schema del database espresso come lista di entità, proprietà e relazioni fra esse"
    )


class CypherTranslation(BaseModel):
    """Result of a text-to-cypher translation."""

    query: str | None = Field(
        description="La query Cypher finale generata, senza markdown o testo aggiuntivo"
    )
    description: str | None = Field(
        description="Descrizione sintetica della query prodotta. Campo obbligatorio nel caso in cui ci sia la query."
    )
    note: str | None = Field(
        description="Nota sintetica opzionale sulla query prodotta."
    )
    error: str | None = Field(
        description="Descrizione di un eventuale errore incontrato durante il processo di traduzione"
    )


class Attempt(BaseModel):
    """CypherTranslation and the error produced in the validation node."""

    generated_cypher: CypherTranslation = Field(
        description="Query cypher generata per instruction"
    )
    db_error: str | None = Field(
        description="Errore generato dalla validazione su database"
    )
    db_warnings: list[str] | None = Field(
        description="Warning non invalidanti generati dalla validazione su databse"
    )


class AttemptsRecord(BaseModel):
    """Attempt list."""

    attempts: list[Attempt] = Field(
        description="Tentativi di traduzione eseguiti per instruction"
    )


class GraphState(TypedDict):
    """Input state for the agent."""

    instruction: str  # user input
    generated_cypher: CypherTranslation | None  # translated query
    is_valid: bool | None
    final_warnings: list[str] | None
    final_error: str | None
    final_note: str | None
    attempts: AttemptsRecord
    retrieved_entities: Entities | None
    retrieved_examples: Examples | None
    retrieved_schema: DBSchema | str | None
    ontology_endpoint: str | None
    try_count: int


def create_init_state(instruction: str, ontology_endpoint: str | None) -> GraphState:
    """Return the init state."""
    attempts = AttemptsRecord(attempts=[])
    init_state = {
        "instruction": instruction,
        "try_count": 0,
        "attempts": attempts,
        "ontology_endpoint": ontology_endpoint,
    }

    return cast(GraphState, init_state)
