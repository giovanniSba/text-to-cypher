from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate

from src.model.configuration import DEFAULT_MODEL_ID
from src.model.model import model


def create_translator_agent():
    """Create a translator from text to cypher."""
    # retrieve system prompt
    system_template = ""
    with open("translator_system_prompt.txt", encoding="utf-8") as f:
        system_template = f.read()

    lang_syntax = ""
    with open("syntax_placeholder.txt", encoding="utf-8") as f:
        lang_syntax = f.read()

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_template),
        ]
    )

    system_prompt_value = prompt.invoke({"lang_syntax": lang_syntax})
    print(system_prompt_value)

    agent = create_agent(model, system_prompt="")

    return agent
