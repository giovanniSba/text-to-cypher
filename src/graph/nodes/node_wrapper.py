import functools

from loguru import logger

from src.graph.state import GraphState


def node_wrapper(node_func):
    """Node for centralized error handling and logging."""

    @functools.wraps(node_func)  # keep __name__ and __module__
    def wrapper(state: GraphState, *args, **kwargs):
        node_name = node_func.__name__
        module_name = node_func.__module__
        node_logger = logger.patch(
            lambda record: record.update(function=node_name, name=module_name)
        )

        node_logger.trace(f"[START NODE] {node_name}")
        try:
            state_update = node_func(state, *args, **kwargs)
            node_logger.trace(f"[END NODE] {node_name}")
            node_logger.info(f"Node update: {state_update}")

            return state_update
        except Exception as e:
            error_str = f"[{node_func.__name__}]Error: {str(e)}"
            node_logger.error(error_str)
            return {"final_error": error_str}

    return wrapper
