from langgraph.checkpoint.serde.types import Value
from langgraph.pregel.protocol import RunnableConfig

from src.graph.config import AppDependencies
from src.graph.state import DBSchema, Entities, EntitiesRecord, GraphState


def entity_retriever(state: GraphState, config: RunnableConfig) -> dict:
    """Extract correct entities from DB schema."""
    configurable = config.get("configurable", {})
    deps: AppDependencies = configurable["deps"]
    instruction = state.get("instruction", "")

    db_schema = state.get("retrieved_schema")
    if db_schema is None:
        raise ValueError()

    entity_set = Entities(inner=set(db_schema.inner.keys()))
    agent = deps.entity_agent

    text = f"AllowedClass: {entity_set}\nInstruction: {instruction}"

    retrieved_entities = agent.retrieve_entities(text)
    # filtered_entities = [
    #     ent
    #     for ent in retrieved_entities.inner
    #     if ent not in already_retrieved_entities.inner
    # ]  # filter entities to keep only the new ones
    # entities_record.last_added_entities = Entities(inner=set(filtered_entities))
    return {
        "entities_record": retrieved_entities,
        "entity_retr_count": state.get("entity_retr_count", 0) + 1,
    }
