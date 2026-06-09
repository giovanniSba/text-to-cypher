import json

from langgraph.pregel.protocol import RunnableConfig

from api import AppDependencies
from src.graph.config import GraphConfig
from src.graph.state import DBEntity, DBSchema, GraphState


def schema_retriever(state: GraphState, config: RunnableConfig) -> dict:
    """Retrieve the schema from the schema vector DB."""
    configurable = config.get("configurable", {})
    deps: AppDependencies = configurable["deps"]
    graph_config: GraphConfig = configurable["graph_config"]

    vectorstore = deps.schema_store
    raw_entities = state.get("retrieved_entities", None)

    if raw_entities is None:
        raise ValueError("Error: retrieved empty is None.")

    entities = raw_entities.entities

    chunks: dict[str, DBEntity] = {}

    for entity in entities:
        result = vectorstore.similarity_search(entity, k=graph_config.schema_k_value)
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
