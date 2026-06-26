import json

MANIFEST_FILE = "workflow_manifest.json"
OUTPUT_FILE = "workflows.json"

if __name__ == "__main__" :
    
    print(f"Reading {MANIFEST_FILE}...")
    with open(MANIFEST_FILE, "r") as f:
        manifest = json.load(f)
    
    count = 0
    workflows = []

    for item in manifest:
        for workflow in item["workflows"]:
            workflows.append(workflow)
            count += 1
    
    print(f"Writing to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, "w") as f:
        json.dump(workflows, f)
    
    print(f"Finished writing {count} workflows to {OUTPUT_FILE}")
