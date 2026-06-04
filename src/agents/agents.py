import os

from agents.entity_retriever_agent import EntityRetrieverAgent
from agents.translator_agent import TranslatorAgent
from model.model import get_model

_entity_retriever_agent = None
_translator_agent = None

ENTITY_RETRIEVER_SYSTEM_PROMPT_PATH = os.environ.get(
    "ENTITY_RETRIEVER_SYSTEM_PROMPT_PATH", ""
)

TRANSLATOR_SYSTEM_PROMPT_PATH = os.environ.get("TRANSLATOR_SYSTEM_PROMPT_PATH", "")


def get_entity_retriever_agent():
    """Singleton instance of entity retriever agent."""
    global _entity_retriever_agent
    if _entity_retriever_agent is None:
        _entity_retriever_agent = EntityRetrieverAgent(
            ENTITY_RETRIEVER_SYSTEM_PROMPT_PATH, get_model()
        )
    return _entity_retriever_agent


def get_translator_agent():
    """Singleton instance of translator agent."""
    global _translator_agent
    if _translator_agent is None:
        _translator_agent = TranslatorAgent(TRANSLATOR_SYSTEM_PROMPT_PATH, get_model())
    return _translator_agent
