# ISE Lab — Summer 2026 Research

Summer 2026 research projects, experiments, and documentation for the ISE/SR Lab at the University of Saskatchewan.  
Work focuses on agentic frameworks for scientific workflows and tooling for platforms such as Galaxy, Nextflow, Snakemake, and VizScieFlow.

## Repo scope
This repository contains multiple projects for the summer research program. Current projects:
- `forum_scraping` — tools to collect topics/posts from Discourse forums (Galaxy, Nextflow)
- `MAGWRAF` — a multi-agent framework for Galaxy workflow retrieval and generation
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


## Contact / Attribution
ISE/SR Lab — University of Saskatchewan  
Summer 2026 research materials and code.