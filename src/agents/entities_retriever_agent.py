from pathlib import Path
from typing import cast

from dotenv.main import logger
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.system import SystemMessage
from langchain_core.runnables.passthrough import RunnableAssign
from langgraph.graph.state import Runnable
from pydantic import BaseModel, Field

from graph.state import EntitiesOutput


class EntitiesRetrieverAgent:
    """Entities retriver agent."""

    _model: BaseChatModel
    _system_prompt: str

    def __init__(self, system_prompt_path: str, model):
        """Create an entities retriever agent."""
        self._model = model
        prompt_file = Path(system_prompt_path)

        if not prompt_file.is_file():
            logger.error(f"Il file di prompt non esiste o non è valido: {prompt_file}")
            raise FileNotFoundError(f"Impossibile trovare {prompt_file}")

        try:
            self._system_prompt = prompt_file.read_text(encoding="utf-8")
        except Exception as e:
            logger.error(f"Error trying to read {prompt_file}: {e}")
            raise

    def retrieve_entities(self, text: str) -> EntitiesOutput:
        """Retrieve entities from text."""
        structured_model = self._model.with_structured_output(EntitiesOutput)
        response = structured_model.invoke(
            [SystemMessage(self._system_prompt), HumanMessage(text)]
        )

        return cast(EntitiesOutput, response)
