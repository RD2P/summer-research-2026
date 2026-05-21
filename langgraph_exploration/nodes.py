from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage

from state import AgentState
from tools import TOOLS

SYSTEM_PROMPT = """You are a quick assistant. You give concise answers as quickly as possible.
Use the calculator for math.
"""

llm = ChatOllama(
    model="qwen3.5:9b",
    base_url="http://localhost:4378", 
    temperature=0,
)

llm_with_tools = llm.bind_tools(TOOLS)


def call_model(state: AgentState) -> dict:
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {
        "messages": [response],
        "iteration": state.get("iteration", 0) + 1,
    }