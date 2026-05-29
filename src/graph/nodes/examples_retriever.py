from langchain_chroma.vectorstores import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langgraph.graph.message import TypedDict

from model.model import embeddings_model
from src.graph.state import GraphState, QueryExample

vectorstore = Chroma(
    persist_directory="./training_examples_db", embedding_function=embeddings_model
)


def examples_retriever(state: GraphState) -> dict:
    """Extract correct entities from DB schema."""
    instruction = state["instruction"]
    result = vectorstore.similarity_search(instruction, k=5)

    examples: list[QueryExample] = []
    for doc in result:
        example: QueryExample = {
            "instruction": doc.metadata.get("instruction", ""),
            "expected": doc.metadata.get("expected", ""),
        }

        examples.append(example)

    print(examples)
    return {"retrieved_examples": examples}
