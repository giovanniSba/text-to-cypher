import os

from dotenv import load_dotenv
from loguru import logger

from src.graph.graph import build_graph
from src.graph.state import GraphConfig, create_init_state
from utils.neo4j import close_driver

load_dotenv()
logger.add("text-to-cypher.log", rotation="20 MB")
ONTOLOGY_ENDPOINT = os.environ.get("ONTOLOGY_ENDPOINT")


def main():
    """Entry point."""
    instruction = input("Query: ")
    init_state = create_init_state(
        instruction,
        GraphConfig(),
    )

    graph = build_graph()

    final_state = graph.invoke(init_state)
    logger.info(f"{final_state}")

    query = final_state.get("generated_cypher", "")
    error = final_state.get("final_error", "")
    try_count = final_state.get("try_count", "")
    warnings = final_state.get("final_warnings")
    logger.info(
        f"\nQuery: {query.query}\nFinal note: {query.note}\nFinal error: {error}\nFinal warning: {warnings}\nTry: {try_count}\nGenerated: {final_state.get('attempts').attempts}"
    )
    # generate graph png image
    png_data = graph.get_graph().draw_mermaid_png()
    with open("grafo.png", "wb") as f:
        f.write(png_data)
    close_driver()


if __name__ == "__main__":
    main()
