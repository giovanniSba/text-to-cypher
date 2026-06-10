from langgraph.pregel.protocol import RunnableConfig

from src.graph.config import AppDependencies
from src.graph.state import DBSchema, Entities, EntitiesRecord, GraphState


def entity_retriever(state: GraphState, config: RunnableConfig) -> dict:
    """Extract correct entities from DB schema."""
    configurable = config.get("configurable", {})
    deps: AppDependencies = configurable["deps"]

    entities_record = state.get("entities_record") or EntitiesRecord()

    already_retrieved_entities: Entities = entities_record.retrieved_entities
    last_entities: Entities = entities_record.last_added_entities
    agent = deps.entity_agent

    schema = state.get("retrieved_schema")
    match schema:
        case DBSchema():
            filtered_schema = [
                ent for ent in schema.db_schema if ent.name in last_entities.inner
            ]
            text = f"Schema:\n{DBSchema(db_schema=filtered_schema)}\nAlreadyRetrieved: {already_retrieved_entities.inner}"  # search only for new detected entities
            # text = f"Schema: \n{schema}"
        case _:
            text = state["instruction"]
    print(f"=================TESTO\n{text}")

    retrieved_entities = agent.retrieve_entities(text)
    filtered_entities = [
        ent
        for ent in retrieved_entities.inner
        if ent not in already_retrieved_entities.inner
    ]  # filter entities to keep only the new ones
    entities_record.last_added_entities = Entities(inner=set(filtered_entities))
    print(f"last added: {entities_record.last_added_entities.inner}")
    return {
        "entities_record": entities_record,
        "entity_retr_count": state.get("entity_retr_count", 0) + 1,
    }
