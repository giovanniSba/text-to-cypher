"""LangGraph single-node graph template.

Returns a predefined response. Replace logic and configuration as needed.
"""

from __future__ import annotations

from typing import Any

from langgraph.constants import START
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph
from typing_extensions import TypedDict

from graph.nodes.schema_retriever import schema_retriever
from src.graph.nodes.cypher_generator import cypher_generator
from src.graph.nodes.db_validator import db_validator
from src.graph.nodes.entity_retriever import entity_retriever
from src.graph.nodes.example_retriever import example_retriever
from src.graph.nodes.router import validator_router
from src.graph.state import GraphState


class Context(TypedDict):
    """Context parameters for the agent."""

    my_configurable_param: str


def build_graph() -> CompiledStateGraph[GraphState, Any]:
    """Return a compiled graph."""
    builder = StateGraph(GraphState, context_schema=Context)
    builder.add_node("entity_retriever", entity_retriever)
    builder.add_node("schema_retriever", schema_retriever)
    builder.add_node("example_retriever", example_retriever)
    builder.add_node("cypher_generator", cypher_generator)
    builder.add_node("db_validator", db_validator)

    builder.add_edge(START, "entity_retriever")
    builder.add_edge("entity_retriever", "schema_retriever")
    builder.add_edge("schema_retriever", "example_retriever")
    builder.add_edge("example_retriever", "cypher_generator")
    builder.add_edge("cypher_generator", "db_validator")
    builder.add_conditional_edges("db_validator", validator_router)

    return builder.compile(name="ttc-graph")
