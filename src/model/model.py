import os
from typing import cast

from langchain.chat_models import init_chat_model
from langchain_google_genai import GoogleGenerativeAIEmbeddings

DEFAULT_MODEL_ID: str = os.environ.get("DEFAULT_MODEL_ID", "")
EMBEDDINGS_MODEL_ID: str = os.environ.get("EMBEDDINGS_MODEL_ID", "")
TEMPERATURE: int = cast(int, os.environ.get("TEMPERATURE", 0))
TOP_P: float = cast(float, os.environ.get("TOP_P", 0.9))

_model = None
_embedding_model = None


def get_model():
    """Singleton instance for LLM."""
    global _model
    if _model is None:
        _model = init_chat_model(
            model=DEFAULT_MODEL_ID,
            temperature=TEMPERATURE,
        )

    return _model


def get_embedding_model():
    """Singleton instance for embedding model."""
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = GoogleGenerativeAIEmbeddings(model=EMBEDDINGS_MODEL_ID)
    return _embedding_model
