# ISE Lab — Summer 2026 Research

Summer 2026 research projects, experiments, and documentation for the ISE/SR Lab at the University of Saskatchewan.  
Work focuses on agentic frameworks for scientific workflows and tooling for platforms such as Galaxy, Nextflow, Snakemake, and VizScieFlow.

## Repo scope
This repository contains multiple projects for the summer research program. Current projects:
- forum_scraping — tools to collect topics/posts from Discourse forums (Galaxy, Nextflow)
- (future) agent prototypes, workflow tooling, benchmarks, docs

## Project: forum_scraping
Location: `forum_scraping/`

Purpose: collect topic metadata and full posts from Discourse-based forums to support analysis and agent experiments.

Quick usage:
```bash
# in main.py:
# 1 set FORUM_KEY to "galaxy" or "nextflow"
# 2 uncomment desired steps in data collection pipeline

python forum_scraping/main.py
```

Primary outputs (per forum):
- `*_results/all_topics.json` — flat list of topic metadata
- `*_results/all_posts.json` — streamed topic posts (large)
- `*_results/final_output.json` — joined dataset (topic + first post cooked)

### Notes
- Scripts use polite delays and `no_definitions=true` to reduce payload.
- Documentation for collection strategy and summary of forum topics/counts/number of requests are in forum_scraping/

## Project: MAGWRAF
Location: `MAGWRAF/`

Purpose: A Multi-Agent Galaxy Workflow Retrieval and Assembly Framework that suggests valid Galaxy workflows from plain English user prompts.

Quick usage:
```bash
# from the MAGWRAF/ directory
python -m app.main "Define a bulk RNA-seq differential expression workflow."
```
See the [project README](./MAGWRAF/README.md) for full details and installation instructions.

## Project: Fine Tuning Data

Location: `fine_tuning_data/`

Purpose: Curate WorkflowHub Galaxy workflows into a compact dataset for LLM fine-tuning and retrieval tasks.

Source: Collected from WorkflowHub on June 4, 2026 (https://www.workflowhub.eu/).

Contents:
- Total workflows: 1479
- Galaxy workflows: 754
- Key files:
    - [fine_tuning_data/example_1713.json](fine_tuning_data/example_1713.json), 
    - [fine_tuning_data/galaxy_workflows.jsonl](fine_tuning_data/galaxy_workflows.jsonl),
    - [fine_tuning_data/galaxy_workflows_summary.json](fine_tuning_data/galaxy_workflows_summary.json)

Scripts:
- Data collection / processing: `fine_tuning_data/main.py`
- Run locally:
```bash
python fine_tuning_data/main.py
```

API Endpoints Used:
- `https://www.workflowhub.eu/workflows.json` — all workflows
- `https://www.workflowhub.eu/workflows.json?filter[workflow_type]=galaxy` — filtered (Galaxy)
- `https://workflowhub.eu/workflows/<id>.json` — individual workflow 
    (example: `https://workflowhub.eu/workflows/1713.json`)

Format / Usage:
- Data is stored as JSON / JSONL (one record per line) suitable for standard fine-tuning pipelines.

More info: See the dataset README for full details: [fine_tuning_data/README.md](fine_tuning_data/README.md)

## Contact / Attribution
ISE/SR Lab — University of Saskatchewan  
Summer 2026 research materials and code.