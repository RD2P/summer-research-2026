from langgraph.graph import END, START, StateGraph

from semantic_planner import plan_semantic_workflow
from planner_llm import refine_plan
from validate import validate_workflow_plan
from state import PlannerState


def run_planner_llm(state: PlannerState) -> dict:
    prompt = state.get("prompt", "")
    base_plan = plan_semantic_workflow(prompt)
    enriched = refine_plan(prompt, base_plan)
    if not enriched.get("matched_tools"):
        enriched["matched_tools"] = base_plan.get("matched_tools", [])
    if not enriched.get("steps"):
        enriched["steps"] = base_plan.get("steps", [])
    if not enriched.get("task_topology"):
        enriched["task_topology"] = base_plan.get("task_topology", [])
    return {
        "workflow_plan": enriched,
        "iteration": state.get("iteration", 0) + 1,
    }


def run_validator(state: PlannerState) -> dict:
    plan_out = validate_workflow_plan(state.get("workflow_plan", {}))
    return {
        "workflow_plan": plan_out,
        "iteration": state.get("iteration", 0) + 1,
    }


builder = StateGraph(PlannerState)
builder.add_node("llm_planner", run_planner_llm)
builder.add_node("validator", run_validator)
builder.add_edge(START, "llm_planner")
builder.add_edge("llm_planner", "validator")
builder.add_edge("validator", END)

graph = builder.compile()
