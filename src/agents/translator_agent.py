import textwrap
from string import Template
from typing import Any

from langchain.agents import create_agent
from langchain.agents.middleware.types import AgentState, ResponseT
from langchain.chat_models.base import init_chat_model
from langchain_core.messages.human import HumanMessage
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
)
from langgraph.graph.state import CompiledStateGraph, Runnable
from pydantic import BaseModel

from src.model.model import model


class TranslateRequest(BaseModel):
    instruction: str
    retrieved_examples: list[Any]
    retrieved_entities: list[Any]


class TranslatorAgent:
    """Text-to-cypher translator agent."""

    _system_prompt: str
    _lang_syntax: str
    _model: Runnable

    def __init__(self):
        """Create a translator for text to cypher."""
        # retrieve system prompt
        system_prompt_template = ""
        with open("translator_system_prompt.txt", encoding="utf-8") as f:
            system_prompt_template = f.read()

        self._lang_syntax = ""
        with open("syntax_placeholder.txt", encoding="utf-8") as f:
            self._lang_syntax = f.read()

        template = Template(system_prompt_template)
        self._system_prompt = template.substitute(lang_syntax=self._lang_syntax)

        self._model = model

    def translate(self, translate_request: TranslateRequest):
        system_message_prompt = SystemMessagePromptTemplate.from_template(
            self._system_prompt, template_format="jinja2"
        )

        human_message_prompt = HumanMessagePromptTemplate.from_template(
            "Traduci: {{instruction}}", template_format="jinja2"
        )

        request_prompt_template = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )

        translator_chain = request_prompt_template | self._model
        response = translator_chain.invoke(translate_request)

        return response
