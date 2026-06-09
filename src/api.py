from typing import cast

from fastapi import Depends, FastAPI, HTTPException
from langchain_chroma.vectorstores import Chroma
from langchain_core.language_models import BaseChatModel
from langgraph.pregel.protocol import RunnableConfig
from loguru import logger
from neo4j import Driver
from pydantic import BaseModel

from agents.agents import get_entity_retriever_agent, get_translator_agent
from graph.config import AppDependencies
from model.model import get_llm
from src.graph.config import GraphConfig
from src.graph.graph import build_graph
from src.graph.state import CypherTranslation, create_init_state
from utils.neo4j import get_neo4j_driver
from utils.vector_stores import get_example_store, get_schema_store

app = FastAPI(title="text-to-cypher API")
logger.add("text-to-cypher.log", rotation="5MB")


def get_app_dependencies(
    neo4j_driver: Driver = Depends(get_neo4j_driver),
    schema_store: Chroma = Depends(get_schema_store),
    example_store: Chroma = Depends(get_example_store),
    llm: BaseChatModel = Depends(get_llm),
) -> AppDependencies:
    """Return an instance of AppDependencies."""
    # agents
    entity_agent = get_entity_retriever_agent(llm)
    translator_agent = get_translator_agent(llm)

    return AppDependencies(
        neo4j_driver=neo4j_driver,
        schema_store=schema_store,
        example_store=example_store,
        entity_agent=entity_agent,
        translator_agent=translator_agent,
    )


class ApiTranslateRequest(BaseModel):
    """Translate request model for FastAPI."""

    nl_query: str
    config: GraphConfig | None = GraphConfig()


class TranslationResponse(BaseModel):
    """Tranlsation response model for FastAPI."""

    query: CypherTranslation
    error: str | None
    warnings: list[str] | None
    try_count: int = 0


@app.post("/translate", response_model=TranslationResponse)
async def translate_text_to_cypher(
    request: ApiTranslateRequest, deps: AppDependencies = Depends(get_app_dependencies)
):
    """Endpoint for text-to-cypher translation."""
    logger.info(f"[Request received] {request}")

    try:
        init_state = create_init_state(request.nl_query)

        # create context
        config = RunnableConfig(
            configurable={
                "deps": deps,
                "graph_config": request.config,
            }
        )

        final_state = build_graph().invoke(init_state, config=config)

        query: CypherTranslation = cast(
            CypherTranslation, final_state.get("generated_cypher")
        )
        final_error = final_state.get("final_error", "")
        final_warnings = final_state.get("final_warnings", [])
        try_count = final_state.get("try_count", 0)

        logger.success(final_state)

        return TranslationResponse(
            query=query, error=final_error, warnings=final_warnings, try_count=try_count
        )
    except Exception as e:
        logger.error(f"Error during API reponse: {e}")
        raise HTTPException(status_code=500, detail=str(e))
