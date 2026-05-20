from langchain_core.tools import tool

@tool
def calculator(expression: str) -> str:
    """Evaluate a basic arithmetic expression. Supports + - * / and parentheses."""
    allowed = set("0123456789+-*/(). ")
    if not set(expression) <= allowed:
        return "Error: only digits and + - * / ( ) . are allowed."
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as exc:
        return f"Error: {exc}"

TOOLS = [calculator]