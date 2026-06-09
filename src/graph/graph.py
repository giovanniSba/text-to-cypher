"""LangGraph single-node graph template.

Returns a predefined response. Replace logic and configuration as needed.
"""

from __future__ import annotations

from typing import Any

from langgraph.constants import END, START
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph

from graph.nodes.output_node import output_formatter
from src.graph.nodes.cypher_generator import cypher_generator
from src.graph.nodes.db_validator import db_validator
from src.graph.nodes.entity_retriever import entity_retriever
from src.graph.nodes.error_nodes import error_handler
from src.graph.nodes.example_retriever import example_retriever
from src.graph.nodes.external_schema_fetcher import external_schema_fetcher
from src.graph.nodes.node_wrapper import node_wrapper
from src.graph.nodes.router import (
    cypher_generation_router,
    global_router,
    schema_router,
    validator_router,
)
from src.graph.nodes.schema_retriever import schema_retriever
from src.graph.state import GraphState


def build_graph() -> CompiledStateGraph[GraphState, Any]:
    """Return a compiled graph."""
    builder = StateGraph(GraphState)
    builder.add_node("external_schema_fetcher", node_wrapper(external_schema_fetcher))
    builder.add_node("entity_retriever", node_wrapper(entity_retriever))
    builder.add_node("schema_retriever", node_wrapper(schema_retriever))
    builder.add_node("example_retriever", node_wrapper(example_retriever))
    builder.add_node("cypher_generator", node_wrapper(cypher_generator))
    builder.add_node("db_validator", node_wrapper(db_validator))
    builder.add_node("error_handler", node_wrapper(error_handler))
    builder.add_node("output_formatter", node_wrapper(output_formatter))

    builder.add_edge(START, "example_retriever")
    builder.add_conditional_edges(
        "example_retriever",
        schema_router,
        ["entity_retriever", "external_schema_fetcher"],
    )
    builder.add_conditional_edges(
        "external_schema_fetcher",
        lambda state: global_router(state, "cypher_generator"),
        ["cypher_generator", "error_handler"],
    )

    builder.add_conditional_edges(
        "entity_retriever",
        lambda state: global_router(state, "schema_retriever"),
        ["schema_retriever", "error_handler"],
    )
    builder.add_conditional_edges(
        "schema_retriever",
        lambda state: global_router(state, "cypher_generator"),
        ["cypher_generator", "error_handler"],
    )

    builder.add_conditional_edges(
        "cypher_generator",
        lambda state: cypher_generation_router(state),
        ["db_validator", "error_handler", "entity_retriever"],
    )
    builder.add_conditional_edges(
        "db_validator",
        validator_router,
        ["output_formatter", "error_handler", "cypher_generator"],
    )
    builder.add_edge("output_formatter", END)

    return builder.compile(name="ttc-graph")
