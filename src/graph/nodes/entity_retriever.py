from agents.agents import get_entity_retriever_agent
from src.graph.state import GraphState


def entity_retriever(state: GraphState) -> dict:
    """Extract correct entities from DB schema."""
    print("====ENTITIES RETRIEVER NODE STATE====")
    print(state)
    agent = get_entity_retriever_agent()
    text = state["instruction"]

    retrived_entities = agent.retrieve_entities(text)

    return {"retrieved_entities": retrived_entities}
