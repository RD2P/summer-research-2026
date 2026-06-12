# Multi-Agent Galaxy Workflow Retrieval and Assembly Framework

## Project Overview

Create a multi-agent framework that suggests valid Galaxy workflows from plain English user prompts.

### Input
Plain English prompts

Example:

```text
Analyze bulk RNA-seq reads and identify differential expression
```

### Workflow Output Format
- Natural language workflow description
- Ordered list of Galaxy tools

Example output:

  Workflow: bulk_rnaseq_differential_expression_pipeline
  Intent: bulk RNA-seq differential expression analysis with quality control

  Steps:
  1. quality_control -> FastQC
  2. trimming -> Trimmomatic
  3. alignment -> STAR
  4. read_counting -> featureCounts
  5. differential_expression_analysis -> edgeR

  Explanation: this workflow follows a standard RNA-seq analysis path, moving from quality control to trimming, alignment, counting, and differential expression.

### Framework Requirements
- Suggest only existing Galaxy tools
- Ensure tool compatibility
- All workflows are runnable
- Retrieve and adapt existing workflows
- Maintain session memory

### Workflow Validation
- Matching datatype extensions
- Semantic compatibility
- Existing workflow patterns

### Architecture
https://excalidraw.com/#json=33sWbMnjd3SnmK0hr2UDf,U9Lk8FWoDsIvN84chaUFWA

### Tool Metadata Structure
```json
{
  "id": "hisat2",
  "name": "HISAT2",
  "description": "...",
  "tool_section_id": "",
  "inputs": ["fastqsanger"],
  "outputs": ["bam"],
  "tasks": []
}
```

### LangGraph Nodes
- retrieve_workflows
- retrieve_tools
- construct_candidate
- validate_types
- critic_review

### Todos
- build tool transition graph
- datatype transition rules
- Design datatype compatibility rules
- Build initial compatibility graph

### Done
- Learn Galaxy API basics
- Choose initial RNA-seq workflow/tool subset
- Extract tool metadata
- Design tool metadata schema
- Build simple json database
- Prototype LangGraph orchestration


### Demo Prep
- Create architecture diagram
- Prepare small curated dataset
- Demonstrate retrieval + planning pipeline
- Demonstrate compatibility validation
- Generate valid RNA-seq workflows from prompts

## Current Semantic Planner

The first executable layer now lives in `app/` and produces a canonical bulk RNA-seq differential expression workflow plan.

Run it from the `MAGWRAF/` directory with:

```bash
python -m app.main "Define a bulk RNA-seq differential expression workflow."
```

The planner returns structured output with:
- `workflow_name`
- `semantic_intent`
- `steps`
- `task_topology`
- `matched_tools`
- `formatted steps and explanation`

## Installation
Requires Python 3.10 or higher

Create a python environment
`python3 -m venv venv`

Activate the environment
`source venv/bin/activate`

You should see (venv) to the left