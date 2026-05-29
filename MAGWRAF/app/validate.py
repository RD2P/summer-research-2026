from __future__ import annotations

from typing import Any

from semantic_planner import load_tool_catalog


def validate_tool_existence(matched_tools: list[dict[str, Any]]) -> tuple[bool, list[dict[str, Any]]]:
	"""Check that every matched tool id exists in the curated tool catalog."""

	catalog = load_tool_catalog()
	catalog_index = {tool.get("id"): tool for tool in catalog}

	details: list[dict[str, Any]] = []
	ok = True

	for matched_tool in matched_tools:
		tool_id = matched_tool.get("tool_id")
		if not tool_id:
			details.append({"type": "existence", "tool_id": None, "ok": False, "reason": "no tool_id"})
			ok = False
		elif tool_id not in catalog_index:
			details.append({"type": "existence", "tool_id": tool_id, "ok": False, "reason": "tool_id not found in catalog"})
			ok = False
		else:
			details.append({"type": "existence", "tool_id": tool_id, "ok": True})

	return ok, details


def validate_io_compatibility(steps: list[dict[str, Any]], matched_tools: list[dict[str, Any]]) -> tuple[bool, list[dict[str, Any]]]:
	"""Check that adjacent workflow steps have compatible tool inputs and outputs."""

	matched_map = {matched_tool.get("tool_id"): matched_tool for matched_tool in matched_tools if matched_tool.get("tool_id")}

	details: list[dict[str, Any]] = []
	ok = True

	for index in range(len(steps) - 1):
		from_step = steps[index]
		to_step = steps[index + 1]
		from_id = from_step.get("tool_id")
		to_id = to_step.get("tool_id")
		from_outputs = matched_map.get(from_id, {}).get("outputs", [])
		to_inputs = matched_map.get(to_id, {}).get("inputs", [])

		if from_outputs and to_inputs:
			overlap = set(from_outputs) & set(to_inputs)
			if not overlap:
				ok = False
				details.append(
					{
						"type": "io_mismatch",
						"from": from_id,
						"to": to_id,
						"from_outputs": from_outputs,
						"to_inputs": to_inputs,
						"ok": False,
						"reason": "no intersection between outputs and inputs",
					}
				)
			else:
				details.append(
					{
						"type": "io_mismatch",
						"from": from_id,
						"to": to_id,
						"ok": True,
						"intersection": list(overlap),
					}
				)
		else:
			details.append(
				{
					"type": "io_mismatch",
					"from": from_id,
					"to": to_id,
					"ok": None,
					"reason": "missing inputs or outputs metadata",
				}
			)

	return ok, details


def validate_workflow_plan(plan: dict[str, Any]) -> dict[str, Any]:
	"""Attach validation summary and details to a workflow plan."""

	plan_out = dict(plan)
	matched_tools = plan_out.get("matched_tools", [])
	steps = plan_out.get("steps", [])
	missing = [step for step in steps if not step.get("tool_id")]

	existence_ok, existence_details = validate_tool_existence(matched_tools)
	io_ok, io_details = validate_io_compatibility(steps, matched_tools)

	plan_out["validation"] = {
		"matched_tools": len(matched_tools),
		"missing_tool_ids": len(missing),
		"existence_ok": existence_ok,
		"io_ok": io_ok,
		"valid": len(missing) == 0 and existence_ok and io_ok and len(matched_tools) > 0,
	}
	plan_out["validation_details"] = existence_details + io_details
	return plan_out
