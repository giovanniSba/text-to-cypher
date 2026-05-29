from langchain.chat_models import init_chat_model
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from src.model.configuration import DEFAULT_MODEL_ID, EMBEDDINGS_MODEL_ID, TEMPERATURE

model = init_chat_model(
    model=DEFAULT_MODEL_ID,
    temperature=TEMPERATURE,
)

embeddings_model = GoogleGenerativeAIEmbeddings(model=EMBEDDINGS_MODEL_ID)
