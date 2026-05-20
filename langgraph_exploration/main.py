from langchain_core.messages import HumanMessage
from graph import graph

def main() -> None:
    initial = {
        "messages": [HumanMessage(content=
            "How many days are there between May 19th to September 5th?")],
        "research_notes": [],
        "iteration": 0,
    }
    final = graph.invoke(initial)
    print("\n--- FINAL ANSWER ---")
    print(final["messages"][-1].content)
    print(f"\nIterations used: {final['iteration']}")


if __name__ == "__main__":
    main()