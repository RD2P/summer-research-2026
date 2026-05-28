from __future__ import annotations

import json
from pathlib import Path
from typing import Any


WORKFLOW_NAME = "bulk_rnaseq_differential_expression"

RNA_SEQ_MOTIF = [
    {
        "task": "quality_control", 
        "query_terms": ["quality", "qc", "fastq"], 
        "fallback_names": ["FastQC", "QualiMap RNA-Seq QC", "QualiMap Counts QC"]
    },
    {"task": "trimming", "query_terms": ["trim", "filter", "adapter"], "fallback_names": ["Trimmomatic", "Filter Combined Transcripts", "ChiRA collapse"]},
    {"task": "alignment", "query_terms": ["align", "mapper", "mapping", "star", "hisat", "rna seq"], "fallback_names": ["HISAT2", "RNA STAR", "Align reads and estimate abundance", "Salmon quant"]},
    {"task": "read_counting", "query_terms": ["count", "quant", "estimate abundance", "expression matrix"], "fallback_names": ["featureCounts", "Kallisto quant", "tximport", "Build expression matrix", "Salmon quant"]},
    {"task": "differential_expression_analysis", "query_terms": ["differential expression", "de", "limma", "edger", "deseq", "degsea"], "fallback_names": ["DESeq2", "edgeR", "limma", "EGSEA", "Differential expression analysis"]},
]

TASK_LABEL_ALIASES = {
    "quality_control": ["quality_control", "qc"],
    "trimming": ["trimming", "filter"],
    "alignment": ["alignment", "mapping", "mapper"],
    "read_counting": ["read_counting", "quantification", "counting"],
    "differential_expression_analysis": ["differential_expression_analysis", "differential expression", "de"],
}


def load_tool_catalog() -> list[dict]:
    catalog_path = Path(__file__).resolve().parent / "curated_tools.jsonl"
    tools: list[dict] = []
    with catalog_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            tools.append(json.loads(line))
    return tools


def infer_semantic_intent(prompt: str) -> str:
    normalized = prompt.lower()
    if any(keyword in normalized for keyword in ["rna-seq", "rnaseq", "rna data", "differential expression", "expression"]):
        return "bulk RNA-seq differential expression"
    return normalized.strip() or "unknown"


def score_tool(tool: dict[str, Any], query_terms: list[str], fallback_names: list[str]) -> int:
    haystack = " ".join(
        str(tool.get(field, ""))
        for field in ["name", "description", "tool_section_id"]
    ).lower()
    haystack += " " + " ".join(str(task).lower() for task in tool.get("tasks", []))

    score = 0
    for term in query_terms:
        if term in haystack:
            score += 3
    for name in fallback_names:
        if name.lower() in haystack:
            score += 2
    if tool.get("tool_section_id") == "rna_seq":
        score += 1
    if tool.get("tasks"):
        score += 1
    return score


def retrieve_candidate_tools(prompt: str, catalog: list[dict], limit: int = 3) -> list[dict]:
    normalized = prompt.lower()
    candidates: list[dict] = []

    for motif in RNA_SEQ_MOTIF:
        task = motif["task"]
        search_terms = motif["query_terms"]
        fallback_names = motif["fallback_names"]

        ranked = sorted(
            catalog,
            key=lambda tool: score_tool(tool, search_terms + normalized.split(), fallback_names),
            reverse=True,
        )

        selected = [tool for tool in ranked if score_tool(tool, search_terms + normalized.split(), fallback_names) > 0]
        if not selected:
            selected = ranked[:limit]
        else:
            selected = selected[:limit]

        if selected:
            candidates.append(
                {
                    "task": task,
                    "tools": selected,
                }
            )

    return candidates


def build_workflow_from_candidates(candidates: list[dict], prompt: str) -> dict:
    steps = []
    topology = []
    matched_tools = []
    previous_task = None

    for candidate in candidates:
        task = candidate["task"]
        tool = candidate["tools"][0]
        step = {
            "task": task,
            "input_type": "",
            "output_type": "",
            "tool_name": tool.get("name"),
            "tool_id": tool.get("id"),
            "description": tool.get("description", ""),
            "tool_section_id": tool.get("tool_section_id", ""),
        }
        steps.append(step)
        matched_tools.append(
            {
                "task": task,
                "tool_name": tool.get("name"),
                "tool_id": tool.get("id"),
                "tool_section_id": tool.get("tool_section_id"),
                "inputs": tool.get("inputs", []),
                "outputs": tool.get("outputs", []),
            }
        )
        if previous_task is not None:
            topology.append({"from": previous_task, "to": task})
        previous_task = task

    return {
        "workflow_name": WORKFLOW_NAME,
        "semantic_intent": infer_semantic_intent(prompt),
        "steps": steps,
        "task_topology": topology,
        "matched_tools": matched_tools,
        "source": "semantic_planner.curated_tools_jsonl_retrieval",
    }


def plan_semantic_workflow(prompt: str) -> dict:
    catalog = load_tool_catalog()
    candidates = retrieve_candidate_tools(prompt, catalog)
    if not candidates:
        return {
            "workflow_name": "unknown",
            "semantic_intent": infer_semantic_intent(prompt),
            "steps": [],
            "task_topology": [],
            "matched_tools": [],
            "source": "semantic_planner.no_candidates",
        }

    return build_workflow_from_candidates(candidates, prompt)
