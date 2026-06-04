from pathlib import Path
from string import Template
from typing import cast

from dotenv.main import logger
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
    retrieved_schema: DBSchema
    attempts: AttemptsRecord


class TranslatorAgent:
    """Text-to-cypher translator agent."""

    _system_prompt: str  # fixed system prompt
    _lang_syntax: str  # syntax lang
    _model: BaseChatModel  # llm model

    def __init__(
        self,
        system_prompt_path: Path,
        model,
    ):
        """Create a translator for text to cypher."""
        self._model = model
        self._lang_syntax = ""
        self._system_prompt = ""

        prompt_file = Path(system_prompt_path)
        syntax_file = Path("syntax_placeholder.txt")

        if not prompt_file.is_file():
            logger.error(f"Il file di prompt non esiste o non è valido: {prompt_file}")
            raise FileNotFoundError(f"Impossibile trovare {prompt_file}")

        if not syntax_file.is_file():
            logger.error(
                f"Il file di sintassi non esiste o non è valido: {syntax_file}"
            )
            raise FileNotFoundError(f"Impossibile trovare {syntax_file}")

        try:
            system_prompt_template = prompt_file.read_text(encoding="utf-8")
        except Exception as e:
            logger.error(f"Errore durante la lettura di {prompt_file}: {e}")
            raise

        try:
            self._lang_syntax = syntax_file.read_text(encoding="utf-8")
        except Exception as e:
            logger.error(f"Errore durante la lettura di {syntax_file}: {e}")
            raise

        # inject lang syntax
        template = Template(system_prompt_template)
        self._system_prompt = template.safe_substitute(lang_syntax=self._lang_syntax)

    def translate(
        self,
        translate_request: TranslateRequest,
    ) -> CypherTranslation:
        """Translate text-to-cypher function."""
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
                "Riprova a tradurre '{{instruction}}', in precedenza hai prodotto i seguenti tentativi: \n {{attempts}}",
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
