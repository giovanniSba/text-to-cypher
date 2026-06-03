from typing import cast

from langchain_chroma import Chroma

from graph.state import DBEntity, DBSchema, Entities, GraphState
from model.model import embeddings_model

vectorstore = Chroma(
    persist_directory="./onthology_db", embedding_function=embeddings_model
)


def schema_retriever(state: GraphState) -> dict:
    """Retrieve the schema from the schema vector DB."""
    print("====SCHEMA RETRIEVER NODE STATE====")
    print(state)

    entities = state["retrieved_entities"].model_dump().get("entities")

    chunks = {}

    for entity in entities:
        result = vectorstore.similarity_search(entity, k=2)
        for doc in result:
            ent = doc.metadata.get("entity", "")
            chunks[ent] = {
                "name": doc.metadata.get("entity", ""),
                "properties": doc.metadata.get("properties", []),
                "relations": doc.metadata.get("relations", []),
            }
    schema: list[DBEntity] = []
    for _key, ent in chunks.items():
        schema.append(ent)

    retrieved_schema: DBSchema = cast(DBSchema, {"db_schema": schema})
    # print(f"""
    #     ========SCHEMA RICAVATO=========
    #     {chunks}
    #     ================================
    #     """)
    return {"retrieved_schema": retrieved_schema}
