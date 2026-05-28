from src.agents.translator_agent import create_translator_agent
from src.graph.state import AgentState


def cypher_generator(state: AgentState) -> dict:
    """Translate text to cypher."""
    agent = create_translator_agent()
    return {"generated_cyper": "match (c:Clients) return c"}
