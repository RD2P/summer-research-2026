# Multi-Agent Galaxy Workflow Retrieval and Assembly Framework

## Project Overview

Create a multi-agent framework that suggests valid Galaxy workflows from plain English user prompts.

- Initially target public Galaxy instance

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

Validation methods:
- Static type checking
- Human review

### Initial Technical Direction
- Hybrid retrieval + rule-based validation
- LLM for reasoning/planning
- Deterministic compatibility checking
- Avoid model training, autonomous execution, entire Galaxy ToolShed for now

Start with:
- One biological domain (RNA-seq)
- 20 curated tools
- Runnable workflows only

### Proposed Architecture
https://excalidraw.com/#json=KJf4UfIlkmY1kjW7qwr23,2LDHYdrgQ0xCRiSrSklzQA

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

### Recommended Tool Metadata Structure
Example:

```json
{
  "tool_id": "hisat2",
  "name": "HISAT2",
  "description": "...",
  "inputs": ["fastqsanger"],
  "outputs": ["bam"],
  "parameters": {},
  "domain": "rna_seq",
  "tags": ["alignment"]
}
```

Potential uses:
- Search/retrieval
- Validation
- Workflow generation
- Graph traversal

### Stack
- Python
- LangGraph
- SQLite

- BM25 retrieval
- Deterministic Python rules for validation

### Suggested LangGraph Nodes
- parse_prompt
- retrieve_workflows
- retrieve_tools
- construct_candidate
- validate_types
- critic_review
- finalize

### Recommended Autonomy Level
- Semi-autonomous system
- Explicit validation stage
- Human-observable execution pipeline

Avoid initially:
- Recursive self-improving agents
- Dynamic agent spawning
- Autonomous workflow execution

### Galaxy APIs and Resources
Galaxy APIs:
- Galaxy API docs
- BioBlend

Useful Galaxy resources:
- Galaxy Training Network
- WorkflowHub
- Galaxy Europe Workflows

Important APIs/features to investigate:
- Tools
- Workflows
- Histories
- Datatypes
- Workflow import/export

### Recommended Research Strategy
Strong recommendation:
- Harvest existing workflows first.

Build:
- Tool transition graph
- Common workflow motifs
- Datatype transition rules

Use real workflows rather than manually encoding everything.

### 2-Week Proof-of-Concept Goal
Input:

```text
Analyze bulk RNA-seq reads and identify differential expression
```

Output:

1. FastQC
2. Trim Galore
3. HISAT2
4. SAMtools sort
5. featureCounts
6. DESeq2

With:
- Explanations
- Compatibility checks
- Retrieved similar workflows

## TODOs

### Immediate
- Learn Galaxy API basics
- Explore BioBlend
- Choose initial RNA-seq workflow/tool subset
- Collect sample Galaxy workflows
- Extract tool metadata
- Design tool metadata schema
- Design datatype compatibility rules
- Build initial compatibility graph
- Build simple SQLite/Postgres database
- Prototype workflow retrieval
- Prototype LangGraph orchestration
- Define evaluation criteria

### Retrieval / Data
- Investigate Galaxy workflow repositories
- Investigate WorkflowHub datasets
- Build workflow ingestion scripts
- Build tool metadata ingestion scripts
- Experiment with BM25 retrieval
- Investigate embeddings later

### Validation
- Define datatype transition rules
- Define semantic compatibility rules
- Create static workflow validator
- Create workflow critic/reviewer stage

### Architecture
- Finalize agent/node responsibilities
- Decide memory/state representation
- Decide retrieval architecture
- Decide graph representation approach

### Demo Preparation
- Create architecture diagram
- Prepare small curated dataset
- Demonstrate retrieval + planning pipeline
- Demonstrate compatibility validation
- Generate valid RNA-seq workflows from prompts
