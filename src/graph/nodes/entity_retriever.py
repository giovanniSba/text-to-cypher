from langgraph.pregel.protocol import RunnableConfig

from agents.agents import get_entity_retriever_agent
from api import AppDependencies
from src.graph.state import GraphState


def entity_retriever(state: GraphState, config: RunnableConfig) -> dict:
    """Extract correct entities from DB schema."""

    configurable = config.get("configurable", {})
    deps: AppDependencies = configurable["deps"]

    agent = deps.entity_agent
    text = state["instruction"]

    retrived_entities = agent.retrieve_entities(text)

    return {"retrieved_entities": retrived_entities}
