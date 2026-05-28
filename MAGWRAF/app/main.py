import json
import sys

from graph import graph
from output_formatter import format_workflow_summary


def main() -> None:
    # take prompt from arg, fallback
    prompt = " ".join(sys.argv[1:]).strip() or "Define a bulk RNA-seq differential expression workflow."
    final_state = graph.invoke(
        {
            "prompt": prompt,
            "iteration": 0,
        }
    )

    workflow_plan = final_state["workflow_plan"]
    print(json.dumps(workflow_plan, indent=2))
    print()
    print(format_workflow_summary(workflow_plan))


if __name__ == "__main__":
    main()
