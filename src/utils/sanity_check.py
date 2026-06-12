import os

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from pydantic import SecretStr

load_dotenv()

OPEN_WEBUI_URL: str = os.environ.get("OPEN_WEBUI_URL", "http://192.168.1.40:11434")
SCHEMA_COLLECTION_NAME: str = os.environ.get(
    "SCHEMA_COLLECTION_NAME", "schema_collection"
)
SCHEMA_DB_PATH: str = os.environ.get("SCHEMA_DB_PATH", "./schema_db")
EMBEDDINGS_MODEL_ID: str = os.environ.get("EMBEDDINGS_MODEL_ID", "")
OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "")

print(EMBEDDINGS_MODEL_ID)
print(OPEN_WEBUI_URL)
embeddings = OllamaEmbeddings(model=EMBEDDINGS_MODEL_ID, base_url=OPEN_WEBUI_URL)

print("Invio di una singola frase di test alla macchina esterna...")
try:
    # Proviamo a fare l'embedding di una sola frase
    vettore = embeddings.embed_query(
        "Ciao, sto verificando se la connessione funziona."
    )

    print("\n✅ CONNESSIONE RIUSCITA!")
    print(f"Il modello ha risposto correttamente.")
    print(f"Lunghezza del vettore generato: {len(vettore)} dimensioni.")

except Exception as e:
    print("\n❌ ERRORE DI CONNESSIONE!")
    print(f"Dettagli dell'errore: {e}")
