import json
import os

from src.graph.state import DBEntity, DBSchema, GraphState
from utils.vector_stores import get_schema_store


def schema_retriever(state: GraphState) -> dict:
    """Retrieve the schema from the schema vector DB."""
    config = state.get("config_params")
    vectorstore = get_schema_store()
    raw_entities = state.get("retrieved_entities", None)

    if raw_entities is None:
        raise ValueError("Error: retrieved empty is None.")

    entities = raw_entities.entities

    chunks: dict[str, DBEntity] = {}

    for entity in entities:
        result = vectorstore.similarity_search(entity, k=config.schema_k_value)
        for doc in result:
            ent = doc.metadata.get("entity", "")
            chunks[ent] = DBEntity(
                name=ent,
                properties=json.loads(doc.metadata.get("properties", "[]")),
                relations=json.loads(doc.metadata.get("relations", "[]")),
            )
    schema: list[DBEntity] = []
    for _key, ent in chunks.items():
        schema.append(ent)

    retrieved_schema = DBSchema(db_schema=schema)
    return {"retrieved_schema": retrieved_schema}
