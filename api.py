from fastapi import FastAPI, HTTPException
from loguru import logger
from pydantic import BaseModel

app = FastAPI(title="text-to-cypher API")
logger.add("text-to-cypher.log", rotation="5MB")


class ApiTranslateRequest(BaseModel):
    query: str
    ontology_endpoint: str
