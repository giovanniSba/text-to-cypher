"""LangGraph single-node graph template.

Returns a predefined response. Replace logic and configuration as needed.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from IPython.display import Image, display
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph
from langgraph.graph.state import START, CompiledStateGraph
from langgraph.runtime import Runtime
from typing_extensions import TypedDict

from graph.nodes.schema_retriever import schema_retriever
from src.graph.nodes.cypher_generator import cypher_generator
from src.graph.nodes.db_validator import db_validator
from src.graph.nodes.entities_retriever import entities_retriever
from src.graph.nodes.examples_retriever import examples_retriever
from src.graph.nodes.router import validator_router
from src.graph.state import GraphState


class Context(TypedDict):
    """Context parameters for the agent."""

    my_configurable_param: str


def build_graph() -> CompiledStateGraph[GraphState, Any]:
    """Return a compiled graph."""
    builder = StateGraph(GraphState, context_schema=Context)
    builder.add_node("entities_retriever", entities_retriever)
    builder.add_node("schema_retriever", schema_retriever)
    builder.add_node("examples_retriever", examples_retriever)
    builder.add_node("cypher_generator", cypher_generator)
    builder.add_node("db_validator", db_validator)

    builder.add_edge(START, "entities_retriever")
    builder.add_edge("entities_retriever", "schema_retriever")
    builder.add_edge("schema_retriever", "examples_retriever")
    builder.add_edge("examples_retriever", "cypher_generator")
    builder.add_edge("cypher_generator", "db_validator")
    builder.add_conditional_edges("db_validator", validator_router)

    return builder.compile(name="ttc-graph")
