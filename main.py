
from dotenv import load_dotenv

from src.graph.graph import build_graph
from src.graph.state import create_init_state
from utils.neo4j import close_driver

load_dotenv()


def main():
    """Entry point."""
    instruction = input("You: ")
    init_state = create_init_state(instruction)

    graph = build_graph()

    final_state = graph.invoke(init_state)

    print("\n--- FINAL STATE ---")
    print(final_state)

    print("\n\n\n==========================")
    # print(f"{final_state['generated_cypher']}\ttry: {final_state['retry_count']}")

    # generate graph png image
    # png_data = graph.get_graph().draw_mermaid_png()
    # with open("grafo.png", "wb") as f:
    #     f.write(png_data)
    close_driver()


if __name__ == "__main__":
    main()
