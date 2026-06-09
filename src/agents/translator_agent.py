from pathlib import Path
from typing import cast

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from pydantic import BaseModel

from src.graph.state import (
    AttemptsRecord,
    CypherTranslation,
    DBSchema,
    Examples,
)


class TranslateRequest(BaseModel):
    """Translation request model."""

    instruction: str
    retrieved_examples: Examples
    retrieved_schema: DBSchema | str
    attempts: AttemptsRecord
    lang_syntax: str | None


class TranslatorAgent:
    """Text-to-cypher translator agent."""

    _system_prompt: str  # fixed system prompt
    _lang_syntax: str  # syntax lang
    _model: BaseChatModel  # llm model

    def __init__(
        self,
        system_prompt: str,
        model,
    ):
        """Create a translator for text to cypher."""
        self._model = model
        self._lang_syntax = ""
        self._system_prompt = ""

        syntax_file = Path("syntax_placeholder.txt")

        if not syntax_file.is_file():
            raise FileNotFoundError(f"{syntax_file} not found")

        self._system_prompt = system_prompt

        self._lang_syntax = syntax_file.read_text(encoding="utf-8")

    def translate(
        self,
        translate_request: TranslateRequest,
    ) -> CypherTranslation:
        """Translate text-to-cypher function."""
        if translate_request.lang_syntax is None:
            translate_request.lang_syntax = self._lang_syntax

        system_message_prompt = SystemMessagePromptTemplate.from_template(
            self._system_prompt, template_format="jinja2"
        )

        attempts_record = translate_request.attempts
        if not attempts_record.attempts:
            human_message_prompt = HumanMessagePromptTemplate.from_template(
                "Traduci: {{instruction}}", template_format="jinja2"
            )
        else:
            human_message_prompt = HumanMessagePromptTemplate.from_template(
                "Riprova a tradurre '{{instruction}}', in precedenza hai prodotto i seguenti tentativi: \n {{attempts}}\n scrivi nella nota cos'hai cambiato",
                template_format="jinja2",
            )

        request_prompt_template = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )

        structured_model = self._model.with_structured_output(CypherTranslation)
        translator_chain = request_prompt_template | structured_model

        # format system prompt with entities and examples and pass the result to the llm
        response = translator_chain.invoke(translate_request.model_dump())
        return cast(CypherTranslation, response)
