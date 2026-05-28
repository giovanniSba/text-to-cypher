"""LangGraph single-node graph template.

Returns a predefined response. Replace logic and configuration as needed.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph
from langgraph.graph.state import START
from langgraph.runtime import Runtime
from typing_extensions import TypedDict

from src.agent.state import AgentState
from src.nodes.cypher_generator import cypher_generator
from src.nodes.db_validator import db_validator
from src.nodes.entities_retriever import entities_retriever
from src.nodes.examples_retriever import examples_retriever
from src.nodes.router import validator_router
from src.nodes.user_input import user_input


class Context(TypedDict):
    """Context parameters for the agent.

    Set these when creating assistants OR when invoking the graph.
    See: https://langchain-ai.github.io/langgraph/cloud/how-tos/configuration_cloud/
    """

    my_configurable_param: str


# Define the graph
builder = StateGraph(AgentState, context_schema=Context)
builder.add_node("user_input", user_input)
builder.add_node("entities_retriever", entities_retriever)
builder.add_node("examples_retriever", examples_retriever)
builder.add_node("cypher_generator", cypher_generator)
builder.add_node("db_validator", db_validator)

builder.add_edge(START, "user_input")
builder.add_edge("user_input", "entities_retriever")
builder.add_edge("user_input", "examples_retriever")
builder.add_edge("entities_retriever", "cypher_generator")
builder.add_edge("examples_retriever", "cypher_generator")
builder.add_edge("cypher_generator", "db_validator")
builder.add_conditional_edges("db_validator", validator_router)

graph = builder.compile(name="ttc-graph")
