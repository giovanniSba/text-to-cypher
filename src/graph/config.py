from dataclasses import dataclass

from langchain_chroma.vectorstores import Chroma
from langgraph.pregel.main import BaseModel
from neo4j import Driver

from agents.entity_retriever_agent import EntityRetrieverAgent
from agents.translator_agent import TranslatorAgent


@dataclass
class AppDependencies:
    """FastAPI App dependencies."""

    neo4j_driver: Driver
    schema_store: Chroma
    example_store: Chroma
    entity_agent: EntityRetrieverAgent
    translator_agent: TranslatorAgent


class GraphConfig(BaseModel):
    """Graph config params."""

    ontology_endpoint: str | None = None
    enable_owl_parsing: bool = False
    example_k_value: int = 5
    schema_k_value: int = 2
    max_gen_attempts: int = 3
