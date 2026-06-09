import os

from dotenv import load_dotenv
from loguru import logger

from graph.config import GraphConfig
from src.graph.graph import build_graph
from src.graph.state import create_init_state

load_dotenv()
logger.add("text-to-cypher.log", rotation="20 MB")
ONTOLOGY_ENDPOINT = os.environ.get("ONTOLOGY_ENDPOINT")
MODEL_ID = os.environ.get("DEFAULT_MODEL_ID", "")
TEMPERATURE = int(os.environ.get("TEMPERATURE", "0"))
EXAMPLE_K_VALUE = int(os.environ.get("EXAMPLE_K_VALUE", "5"))
SCHEMA_K_VALUE = int(os.environ.get("SCHEMA_K_VALUE", "2"))
MAX_GEN_ATTEMPTS = int(os.environ.get("MAX_GEN_ATTEMPTS", "3"))
ENABLE_OWL_PARSING = os.environ.get("ENABLE_OWL_PARSING", "") in ["True", "true", 1]


def main():
    """Entry point."""
    # instruction = input("Query: ")
    # config = GraphConfig(
    #     enable_owl_parsing=ENABLE_OWL_PARSING,
    #     example_k_value=EXAMPLE_K_VALUE,
    #     max_gen_attempts=MAX_GEN_ATTEMPTS,
    #     ontology_endpoint=ONTOLOGY_ENDPOINT,
    #     schema_k_value=SCHEMA_K_VALUE,
    # )
    # init_state = create_init_state(
    #     instruction,
    # )

    graph = build_graph()

    # final_state = graph.invoke(init_state)
    # logger.info(f"{final_state}")

    # query = final_state.get("generated_cypher", "")
    # error = final_state.get("final_error", "")
    # try_count = final_state.get("try_count", "")
    # warnings = final_state.get("final_warnings")
    # logger.info(
    #     f"\nQuery: {query.query}\nFinal note: {query.note}\nFinal error: {error}\nFinal warning: {warnings}\nTry: {try_count}\nGenerated: {final_state.get('attempts').attempts}"
    # )
    # generate graph png image
    png_data = graph.get_graph().draw_mermaid_png()
    with open("grafo.png", "wb") as f:
        f.write(png_data)


if __name__ == "__main__":
    main()
