from __future__ import annotations

import json
from typing import Any

from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage


# Use Ollama for plan refinement. On any error we return the base plan.
# Uses Ollama set up described in soarserver_ollama_setup.md
llm = ChatOllama(
    model="qwen3.5:9b",
    base_url="http://localhost:4378",
    temperature=0,
)


def refine_plan_with_llm(prompt: str, base_plan: dict) -> dict:
    system = SystemMessage(
        content=(
            "You are a galaxy workflow planner assistant.\n"
            "Receive a user prompt and a base workflow plan (JSON). Return an improved workflow plan as JSON only.\n"
            "Required fields: workflow_name, semantic_intent, steps (list of {task,input_type,output_type,tool_name,tool_id}), task_topology (list of {from,to})."
        )
    )
    human = HumanMessage(content=f"User prompt:\n{prompt}\n\nBase plan:\n{json.dumps(base_plan)}")

    try:
        resp = llm.invoke([system, human])
        text = getattr(resp, "content", None) or str(resp)
        parsed = json.loads(text)
        if isinstance(parsed, dict) and parsed.get("workflow_name"):
            return parsed
    except Exception:
        # Any error -> return base plan unchanged
        return base_plan

    return base_plan


def refine_plan(prompt: str, base_plan: dict) -> dict:
    return refine_plan_with_llm(prompt, base_plan)
