import os
from typing import cast

from langchain.chat_models import init_chat_model
from langchain_ollama import OllamaEmbeddings

DEFAULT_MODEL_ID: str = os.environ.get("DEFAULT_MODEL_ID", "")
EMBEDDINGS_MODEL_ID: str = os.environ.get("EMBEDDINGS_MODEL_ID", "")
TEMPERATURE: int = cast(int, os.environ.get("TEMPERATURE", 0))
TOP_P: float = cast(float, os.environ.get("TOP_P", 0.9))
OPEN_WEBUI_URL: str = os.environ.get("OPEN_WEBUI_URL", "http://192.168.1.40:11434")


def get_llm(model_id: str | None = DEFAULT_MODEL_ID):
    """Create an LLM instance for the request."""
    return init_chat_model(
        model=model_id,
        model_provider="ollama",
        base_url=OPEN_WEBUI_URL,
        temperature=TEMPERATURE,
    )


def get_embedding_model():
    """Create an embedding model instance for the request."""
    return OllamaEmbeddings(
        model=EMBEDDINGS_MODEL_ID,
        base_url=OPEN_WEBUI_URL,
    )
