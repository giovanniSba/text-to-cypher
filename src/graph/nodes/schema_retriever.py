import json

from langgraph.pregel.protocol import RunnableConfig

from src.graph.config import AppDependencies, GraphConfig
from src.graph.state import DBEntity, DBSchema, Entities, EntitiesRecord, GraphState


def schema_retriever(state: GraphState, config: RunnableConfig) -> dict:
    """Retrieve the schema from the schema vector DB."""
    return {}
    # configurable = config.get("configurable", {})
    # deps: AppDependencies = configurable["deps"]
    # graph_config: GraphConfig = configurable["graph_config"]

    # updated_schema: dict = {}
    # already_retrieved_schema = state.get("retrieved_schema")
    # match already_retrieved_schema:
    #     case DBSchema():
    #         updated_schema = already_retrieved_schema.inner
    #     case _:
    #         pass

    # vectorstore = deps.schema_store
    # entities_record = state.get("entities_record") or EntitiesRecord()

    # new_entities = entities_record.last_added_entities.inner

    # schema_update: dict[str, DBEntity] = {}
    # last_entity_added_updated = Entities()

    # # search for only for new entities in the vector DB
    # for entity in new_entities:
    #     result = vectorstore.similarity_search(entity, k=graph_config.schema_k_value)
    #     for doc in result:
    #         ent = doc.metadata.get("entity", "")
    #         last_entity_added_updated.inner.add(
    #             ent
    #         )  # add the actual name of the retrieved entity

    #         schema_update[ent] = DBEntity(
    #             name=ent,
    #             properties=json.loads(doc.metadata.get("properties", "[]")),
    #             relations=json.loads(doc.metadata.get("relations", "[]")),
    #         )

    # for _key, ent in schema_update.items():
    #     updated_schema(ent)

    # entities_record.last_added_entities = last_entity_added_updated
    # entities_record.retrieved_entities.inner = (
    #     entities_record.retrieved_entities.inner | last_entity_added_updated.inner
    # )  # update the retrieved entities

    # retrieved_schema = DBSchema(inner=updated_schema)
    # return {
    #     "retrieved_schema": retrieved_schema,
    #     "entities_record": entities_record,
    # }
