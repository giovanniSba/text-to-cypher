from agents.entities_retriever_agent import EntitiesRetrieverAgent
from model.model import model
from src.graph.state import GraphState


def entities_retriever(state: GraphState) -> dict:
    """Extract correct entities from DB schema."""
    print("====ENTITIES RETRIEVER NODE STATE====")
    print(state)
    agent = EntitiesRetrieverAgent("entities_retriever_system_prompt.txt", model=model)
    text = state["instruction"]

    retrived_entities = agent.retrieve_entities(text)

    return {"retrieved_entities": retrived_entities}
