import json
import os

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

load_dotenv()

OPEN_WEBUI_URL: str = os.environ.get("OPEN_WEBUI_URL", "http://192.168.1.40:11434")
EXAMPLE_COLLECTION_NAME: str = os.environ.get(
    "EXAMPLE_COLLECTION_NAME", "example_collection"
)
EXAMPLE_DB_PATH: str = os.environ.get("EXAMPLE_DB_PATH", "./training_examples_db")
EMBEDDINGS_MODEL_ID: str = os.environ.get("EMBEDDINGS_MODEL_ID", "")

embeddings = OllamaEmbeddings(
    model=EMBEDDINGS_MODEL_ID,
    base_url=OPEN_WEBUI_URL,
)

examples = []
with open("macro_training_dataset.jsonl", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        text = data["input"]

        examples.append(
            {
                "text": text,
                "metadata": {
                    "instruction": data["input"],
                    "expected": data["expected"],
                },
            }
        )

texts = [ex["text"] for ex in examples]
metadata = [ex["metadata"] for ex in examples]

vectorstore = Chroma.from_texts(
    collection_name=EXAMPLE_COLLECTION_NAME,
    texts=texts,
    metadatas=metadata,
    embedding=embeddings,
    persist_directory=EXAMPLE_DB_PATH,
)
