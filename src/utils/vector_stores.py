import os
from functools import lru_cache

from langchain_chroma.vectorstores import Chroma

from model.model import get_embedding_model

EXAMPLE_DB_PATH = os.environ.get("EXAMPLE_DB_PATH", "")
SCHEMA_DB_PATH = os.environ.get("SCHEMA_DB_PATH", "")
SCHEMA_COLLECTION_NAME: str = os.environ.get(
    "SCHEMA_COLLECTION_NAME", "schema_collection"
)
EXAMPLE_COLLECTION_NAME: str = os.environ.get(
    "EXAMPLE_COLLECTION_NAME", "example_collection"
)


@lru_cache(maxsize=1)
def get_example_store():
    """Create an instance for example vector db."""
    return Chroma(
        collection_name=EXAMPLE_COLLECTION_NAME,
        persist_directory=EXAMPLE_DB_PATH,
        embedding_function=get_embedding_model(),
    )


@lru_cache(maxsize=1)
def get_schema_store():
    """Create an instance for schema vector db."""
    return Chroma(
        collection_name=SCHEMA_COLLECTION_NAME,
        persist_directory=SCHEMA_DB_PATH,
        embedding_function=get_embedding_model(),
    )
