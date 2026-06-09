from langgraph.pregel.protocol import RunnableConfig

from api import AppDependencies
from graph.config import GraphConfig
from src.graph.state import Examples, GraphState, QueryExample


def example_retriever(state: GraphState, config: RunnableConfig) -> dict:
    """Extract correct entities from DB schema."""
    configurable = config.get("configurable", {})
    deps: AppDependencies = configurable["deps"]

    graph_config: GraphConfig = configurable["graph_config"]

    vectorstore = deps.example_store
    instruction = state["instruction"]
    result = vectorstore.similarity_search(instruction, k=graph_config.example_k_value)

    examples: list[QueryExample] = []
    for doc in result:
        example: QueryExample = QueryExample(
            instruction=doc.metadata.get("instruction", ""),
            expected=doc.metadata.get("expected", ""),
        )

        examples.append(example)

    retrieved_examples = Examples(examples=examples)
    return {"retrieved_examples": retrieved_examples}
