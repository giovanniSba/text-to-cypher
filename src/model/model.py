from langchain.chat_models import init_chat_model

from src.model.configuration import DEFAULT_MODEL_ID, TEMPERATURE

model = init_chat_model(
    model=DEFAULT_MODEL_ID,
    temperature=TEMPERATURE,
)
