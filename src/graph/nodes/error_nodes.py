from graph.state import GraphState


def error_wrapper(node_func):
    """Node for centralized error handling."""

    def wrapper(state: GraphState, *args, **kwargs):
        try:
            return node_func(state, *args, **kwargs)
        except Exception as e:
            return {"final_error": f"[{node_func.__name__}]Error: {str(e)}"}

    return wrapper


def error_handler(state: GraphState) -> dict:
    print(f"====ERROR NODE HANDLER===={state.get('final_error')}")
    return {}
