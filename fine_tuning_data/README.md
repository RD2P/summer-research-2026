# WorkflowHub Data Collection for Fine-Tuning

This document outlines the process of collecting data from [WorkflowHub](https://www.workflowhub.eu/) for the purpose of fine-tuning a large language model. This effort is part of a larger project to develop a multi-agent framework for Galaxy workflow retrieval and generation.

## Data Source

*   **Website:** [https://www.workflowhub.eu/](https://www.workflowhub.eu/)
*   **Collection Date:** June 4th, 2026

## Data Overview

*   **Total Workflows:** 1479
*   **Galaxy Workflows:** 754

## API Endpoints

The following API endpoints were used to gather the data.

### All Workflows

Returns a JSON list of all public workflows.
```
https://www.workflowhub.eu/workflows.json
```

### Filtered Workflows (Galaxy)

Returns a JSON list of workflows filtered by type (e.g., Galaxy).
```
https://www.workflowhub.eu/workflows.json?filter[workflow_type]=galaxy
```

### Individual Workflow

Returns the full JSON metadata for a specific workflow by its ID.
```
https://workflowhub.eu/workflows/<id>.json
```

**Example:**
```
https://workflowhub.eu/workflows/1713.json
```

## Data Collection Process

1.  A summary of all Galaxy workflows is first retrieved from the `https://www.workflowhub.eu/workflows.json?filter[workflow_type]=galaxy` endpoint and saved as `galaxy_workflows_summary.json`.
2.  This summary file, however, does not contain the full details for each workflow, such as the individual steps.
3.  The `main.py` script reads `galaxy_workflows_summary.json` to extract the ID for each workflow.
4.  For each ID, the script makes an API call to `https://workflowhub.eu/workflows/<id>.json` to fetch the complete workflow data.
5.  This full workflow data is then appended as a new line to the `galaxy_workflows.jsonl` file, creating a JSON Lines dataset where each line is a complete JSON object for a single workflow.