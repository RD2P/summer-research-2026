## Data Sources

- **[IWC Website](https://iwc.galaxyproject.org/)**
  - Contains 121 Galaxy workflows.
  - Maintained by the Intergalactic Workflow Commission (IWC) to ensure high-quality Galaxy workflows.
- **[IWC GitHub Repository](https://github.com/galaxyproject/iwc/tree/main/workflows)**
  - All workflows are curated and peer-reviewed.
  - Includes test data, documentation, versioning, and regular testing.
- **Published Workflow Lists by Instance:**
  - [usegalaxy.org](https://usegalaxy.org/workflows/list_published?owner=iwc)
  - [usegalaxy.eu](https://usegalaxy.eu/workflows/list_published?owner=iwc)
  - [usegalaxy.org.au](https://usegalaxy.org.au/workflows/list_published?owner=iwc)
- **Galaxy Training Material (GTN):**
  - [Training Hub](https://training.galaxyproject.org/training-material/)
  - [Workflow List](https://training.galaxyproject.org/training-material/workflows/list.html)


## Data Collection from iwc.galaxyproject.org

- Collection date: June 16th, 2026
- The website source code is in the github repo: `https://github.com/galaxyproject/iwc/tree/main`

- The website is static, all the data is generated from the repository itself.
- All workflow information is stored in `workflows/`

```
iwc/
└── workflows/
    ├── workflow_A/
    │   ├── .dockstore.yml
    │   ├── workflow.ga
    │   ├── README.md
    │   ├── CHANGELOG.md
    │   └── tests
    └── workflow_B/
```

- The `scripts/workflow_manifest.py` generates the workflow_manifest.json. The manifest is also available at "https://iwc.galaxyproject.org/workflow_manifest.json"

- The manifest, saved in this project, has the following structure:

```json
[
    {
        "version": 1.2,
        "workflows": [
            {
                "name": "SARS-COV-2-ILLUMINA-AMPLICON-IVAR-PANGOLIN-NEXTCLADE",
                "subclass": "Galaxy",
                "primaryDescriptorPath": "/pe-wgs-ivar-analysis.ga",
                "definition": {
                    "name": "SARS-CoV-2 Illumina Amplicon pipeline - iVar based",
                    "readme": "...",
                    "steps": {
                        "0": {...},
                        "25": {...}
                    },
                    "tags": [ "COVID-19", "ARTIC" ],
                },
                "workflow_job_input": {...},
                "readme": "...",
                "categories": ["COVID-19"],
            },
        ],
        "path": "./workflows/sars-cov-2-variant-calling/sars-cov-2-pe-illumina-artic-ivar-analysis"
    },
    ...
]
```

The extraction script `main.py` iterates through all categories and collects every workflow into a single array, resulting in the output file: `workflows.json`
