from typing import cast

from src.graph.state import Examples, GraphState, QueryExample
from utils.vector_stores import get_examples_store


def example_retriever(state: GraphState) -> dict:
    """Extract correct entities from DB schema."""
    vectorstore = get_examples_store()

    instruction = state["instruction"]
    result = vectorstore.similarity_search(instruction, k=5)

    examples: list[QueryExample] = []
    for doc in result:
        example: QueryExample = QueryExample(
            instruction=doc.metadata.get("instruction", ""),
            expected=doc.metadata.get("expected", ""),
        )

        examples.append(example)

    retrieved_examples = Examples(examples=examples)
    return {"retrieved_examples": retrieved_examples}
