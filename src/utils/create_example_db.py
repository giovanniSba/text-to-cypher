import json

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2")

# Carica i dati
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

testi = [ex["text"] for ex in examples]
metadati = [ex["metadata"] for ex in examples]

# CREA E SALVA IL DB SU DISCO
# Specificando persist_directory, Chroma salverà i file fisicamente in quella cartella
vectorstore = Chroma.from_texts(
    collection_name="example_collection",
    texts=testi,
    metadatas=metadati,
    embedding=embeddings,
    persist_directory="./training_examples_db",  # Scegli il nome della cartella
)

print("Database vettoriale creato e salvato con successo!")
