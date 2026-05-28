from __future__ import annotations


def format_workflow_summary(workflow_plan: dict) -> str:
    steps = workflow_plan.get("steps", [])
    semantic_intent = workflow_plan.get("semantic_intent", "workflow")

    lines = []
    lines.append(f"Workflow: {workflow_plan.get('workflow_name', 'unknown')}")
    lines.append(f"Intent: {semantic_intent}")
    lines.append("")

    if not steps:
        lines.append("No workflow steps were found for this prompt.")
        return "\n".join(lines)

    lines.append("Steps:")
    for index, step in enumerate(steps, start=1):
        task = step.get("task", "unknown task")
        tool_name = step.get("tool_name", "unknown tool")
        lines.append(f"{index}. {task} -> {tool_name}")

    lines.append("")
    lines.append(
        "Explanation: this workflow follows a standard RNA-seq analysis path, "
        "moving from quality control to trimming, alignment, counting, and differential expression."
    )
    return "\n".join(lines)
