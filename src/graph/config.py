from dataclasses import dataclass

from langchain_chroma.vectorstores import Chroma
from langgraph.pregel.main import BaseModel
from neo4j import Driver
from pydantic import ConfigDict, Field, HttpUrl

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
    """Graph config parameters."""

    ontology_endpoint: HttpUrl | None = Field(
        default=None,
        description="The URL of the ontology endpoint to retrieve the schema.",
        examples=["http://localhost:8080/ontology"],
    )

    enable_owl_parsing: bool = Field(
        default=False, description="Whether to enable parsing of OWL files."
    )

    example_k_value: int = Field(
        default=5,
        ge=1,
        le=20,
        description="The number of similar Cypher examples to retrieve (K-value).",
    )

    schema_k_value: int = Field(
        default=2,
        ge=1,
        description="The number of schema nodes and relationships to retrieve.",
    )

    max_gen_attempts: int = Field(
        default=3,
        ge=1,
        le=5,
        description="The maximum number of attempts to correct the Cypher query in case of a syntax error.",
    )

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
