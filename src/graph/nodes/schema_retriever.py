import json
from typing import cast

from src.graph.state import DBEntity, DBSchema, GraphState
from utils.vector_stores import get_schema_store


def schema_retriever(state: GraphState) -> dict:
    """Retrieve the schema from the schema vector DB."""
    vectorstore = get_schema_store()
    raw_entities = state.get("retrieved_entities", None)

    if raw_entities is None:
        raise ValueError("Error: retrieved empty is None.")

    entities = raw_entities.entities

    chunks: dict[str, DBEntity] = {}

    for entity in entities:
        result = vectorstore.similarity_search(entity, k=2)
        for doc in result:
            ent = doc.metadata.get("entity", "")
            chunks[ent] = DBEntity(
                name=doc.metadata.get("entity", ""),
                properties=json.loads(doc.metadata.get("properties", "[]")),
                relations=json.loads(doc.metadata.get("relations", "[]")),
            )
    schema: list[DBEntity] = []
    for _key, ent in chunks.items():
        schema.append(ent)

    retrieved_schema = DBSchema(db_schema=schema)
    return {"retrieved_schema": retrieved_schema}
