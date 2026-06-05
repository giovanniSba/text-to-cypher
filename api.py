from typing import cast

from fastapi import FastAPI, HTTPException
from loguru import logger
from pydantic import BaseModel

from src.graph.graph import build_graph
from src.graph.state import CypherTranslation, GraphConfig, create_init_state
from src.utils.neo4j import close_driver

app = FastAPI(title="text-to-cypher API")
logger.add("text-to-cypher.log", rotation="5MB")


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
async def translate_text_to_cypher(request: ApiTranslateRequest):
    """Endpoint for text-to-cypher translation."""
    logger.info(f"[Request received] {request}")

    try:
        init_state = create_init_state(request.nl_query, request.config)

        final_state = build_graph().invoke(init_state)

        query: CypherTranslation = cast(
            CypherTranslation, final_state.get("generated_cypher")
        )
        final_error = final_state.get("final_error", "")
        final_warnings = final_state.get("final_warnings", [])
        try_count = final_state.get("try_count", 0)

        close_driver()
        logger.success(final_state)

        return TranslationResponse(
            query=query, error=final_error, warnings=final_warnings, try_count=try_count
        )
    except Exception as e:
        logger.error(f"Error during API reponse: {e}")
        close_driver()
        raise HTTPException(status_code=500, detail=str(e))
