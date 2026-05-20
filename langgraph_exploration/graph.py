from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

from state import AgentState
from tools import TOOLS
from nodes import call_model


def route_after_model(state: AgentState) -> str:
    last = state["messages"][-1]
    if getattr(last, "tool_calls", None):
        return "tools"
    if state.get("iteration", 0) >= 10:
        return END    # hard safety stop
    return END


builder = StateGraph(AgentState)
builder.add_node("model", call_model)
builder.add_node("tools", ToolNode(TOOLS))

builder.add_edge(START, "model")
builder.add_conditional_edges("model", route_after_model, ["tools", END])
builder.add_edge("tools", "model")

graph = builder.compile()