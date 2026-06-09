from typing import cast

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.system import SystemMessage

from src.graph.state import Entities


class EntityRetrieverAgent:
    """Entities retriver agent."""

    _model: BaseChatModel
    _system_prompt: str

    def __init__(self, system_prompt: str, model):
        """Create an entities retriever agent."""
        self._model = model

        self._system_prompt = system_prompt

    def retrieve_entities(self, text: str) -> Entities:
        """Retrieve entities from text."""
        structured_model = self._model.with_structured_output(Entities)
        response = structured_model.invoke(
            [SystemMessage(self._system_prompt), HumanMessage(text)]
        )

        return cast(Entities, response)
