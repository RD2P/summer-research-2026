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