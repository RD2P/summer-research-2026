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

1. FastQC
2. Trim Galore
3. HISAT2
4. SAMtools sort
5. featureCounts
6. DESeq2

### Framework Requirements
The framework should:
- Suggest only existing Galaxy tools
- Ensure tool compatibility
- All workflows are runnable
- Retrieve and adapt existing workflows
- Maintain session memory

### Workflow Validation
- Matching datatype extensions
- Semantic compatibility
- Existing workflow patterns

### Proposed Architecture
https://excalidraw.com/#json=4eGvxaSpHO4E3zEMVn3mU,OwQm-Dpe-kZngfswjRnbNQ

#### Tool Compatibility Graph
Example:

```text
FASTQ
  ↓
FastQC
  ↓
Trim Galore
  ↓
HISAT2
  ↓
SAMtools
  ↓
featureCounts
```

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