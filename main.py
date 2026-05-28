from typing import cast

from dotenv import load_dotenv
from IPython.display import Image, display

from src.graph.graph import build_graph
from src.graph.state import AgentState

load_dotenv()


def main():
    """Entry point."""
    initial_state = {
        "instruction": "Mostrami tutti i clienti di Milano",
        "retry_count": 0,
        "is_valid": True,
    }

    initial_state = cast(AgentState, {})

    print("Avvio del grafo...")

    graph = build_graph()

    final_state = graph.invoke(initial_state)

    print("\n--- STATO FINALE ---")
    print(final_state)

    display(Image(graph.get_graph().draw_mermaid_png()))


if __name__ == "__main__":
    main()
