import os
from functools import lru_cache
from pathlib import Path

from agents.entity_retriever_agent import EntityRetrieverAgent
from agents.translator_agent import TranslatorAgent

ENTITY_RETRIEVER_SYSTEM_PROMPT_PATH = os.environ.get(
    "ENTITY_RETRIEVER_SYSTEM_PROMPT_PATH", ""
)

TRANSLATOR_SYSTEM_PROMPT_PATH = os.environ.get("TRANSLATOR_SYSTEM_PROMPT_PATH", "")


@lru_cache(maxsize=5)
def get_cached_file_content(file_path: str) -> str:
    """Load a file (cached)."""
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"{path} not found")

    return path.read_text(encoding="utf-8")


def get_entity_retriever_agent(llm) -> EntityRetrieverAgent:
    """Create a new entity retriver agent injecting the model."""
    return EntityRetrieverAgent(
        system_prompt=get_cached_file_content(ENTITY_RETRIEVER_SYSTEM_PROMPT_PATH),
        model=llm,
    )


def get_translator_agent(llm) -> TranslatorAgent:
    """Create a new translator agent injecting the model."""
    return TranslatorAgent(
        system_prompt=get_cached_file_content(TRANSLATOR_SYSTEM_PROMPT_PATH), model=llm
    )
