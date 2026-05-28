from typing import TypedDict


class PlannerState(TypedDict, total=False):
    prompt: str
    workflow_plan: dict
    iteration: int
