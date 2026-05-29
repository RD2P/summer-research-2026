from langgraph.graph import END, START, StateGraph

from semantic_planner import plan_semantic_workflow, load_tool_catalog
from planner_llm import refine_plan
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
    plan = state.get("workflow_plan", {})
    plan_out = dict(plan)
    matched = plan_out.get("matched_tools", [])
    steps = plan_out.get("steps", [])
    missing = [step for step in steps if not step.get("tool_id")]

    # Existence check against the curated tool catalog
    catalog = load_tool_catalog()
    catalog_index = {t.get("id"): t for t in catalog}
    validation_details: list[dict] = []
    existence_ok = True
    for mt in matched:
        tid = mt.get("tool_id")
        if not tid:
            validation_details.append({"type": "existence", "tool_id": None, "ok": False, "reason": "no tool_id"})
            existence_ok = False
        elif tid not in catalog_index:
            validation_details.append({"type": "existence", "tool_id": tid, "ok": False, "reason": "tool_id not found in catalog"})
            existence_ok = False
        else:
            validation_details.append({"type": "existence", "tool_id": tid, "ok": True})

    # I/O compatibility: compare outputs of each step to inputs of the next step
    io_ok = True
    matched_map = {mt.get("tool_id"): mt for mt in matched if mt.get("tool_id")}
    for i in range(len(steps) - 1):
        from_step = steps[i]
        to_step = steps[i + 1]
        from_id = from_step.get("tool_id")
        to_id = to_step.get("tool_id")
        from_outputs = matched_map.get(from_id, {}).get("outputs", [])
        to_inputs = matched_map.get(to_id, {}).get("inputs", [])

        if from_outputs and to_inputs:
            overlap = set(from_outputs) & set(to_inputs)
            if not overlap:
                io_ok = False
                validation_details.append({
                    "type": "io_mismatch",
                    "from": from_id,
                    "to": to_id,
                    "from_outputs": from_outputs,
                    "to_inputs": to_inputs,
                    "ok": False,
                    "reason": "no intersection between outputs and inputs",
                })
            else:
                validation_details.append({
                    "type": "io_mismatch",
                    "from": from_id,
                    "to": to_id,
                    "ok": True,
                    "intersection": list(overlap),
                })
        else:
            # Missing metadata -> cannot determine compatibility
            validation_details.append({
                "type": "io_mismatch",
                "from": from_id,
                "to": to_id,
                "ok": None,
                "reason": "missing inputs or outputs metadata",
            })

    plan_out["validation"] = {
        "matched_tools": len(matched),
        "missing_tool_ids": len(missing),
        "existence_ok": existence_ok,
        "io_ok": io_ok,
        "valid": len(missing) == 0 and existence_ok and io_ok and len(matched) > 0,
    }
    plan_out["validation_details"] = validation_details

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
