import os

from langchain_chroma.vectorstores import Chroma

from model.model import get_embedding_model

_examples_store = None
_schema_store = None

EXAMPLE_DB_PATH = os.environ.get("EXAMPLE_DB_PATH", "")
SCHEMA_DB_PATH = os.environ.get("SCHEMA_DB_PATH", "")


def get_examples_store():
    """Singleton instance for example vector db."""
    global _examples_store
    if _examples_store is None:
        _examples_store = Chroma(
            collection_name="example_collection",
            persist_directory=EXAMPLE_DB_PATH,
            embedding_function=get_embedding_model(),
        )
    return _examples_store


def get_schema_store():
    """Singleton instance for schema vector db."""
    global _schema_store
    if _schema_store is None:
        _schema_store = Chroma(
            collection_name="schema_collection",
            persist_directory=SCHEMA_DB_PATH,
            embedding_function=get_embedding_model(),
        )
    return _schema_store
