from agents.entity_retriever_agent import EntityRetrieverAgent
from model.model import model
from src.graph.state import GraphState


def entity_retriever(state: GraphState) -> dict:
    """Extract correct entities from DB schema."""
    print("====ENTITIES RETRIEVER NODE STATE====")
    print(state)
    agent = EntityRetrieverAgent("entities_retriever_system_prompt.txt", model=model)
    text = state["instruction"]

    retrived_entities = agent.retrieve_entities(text)

    return {"retrieved_entities": retrived_entities}
