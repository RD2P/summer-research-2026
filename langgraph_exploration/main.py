from langchain_core.messages import HumanMessage
from graph import graph
from state import AgentState

def main() -> None:
    initial = AgentState({
        "messages": [
            HumanMessage(content="What is (12 * 5) + 3?")
        ],
        "research_notes": [],
        "iteration": 0,
    })
    final = graph.invoke(initial)
    print("\n--- FINAL ANSWER ---")
    print(final["messages"][-1].content)
    print(f"\nIterations used: {final['iteration']}")


if __name__ == "__main__":
    main()