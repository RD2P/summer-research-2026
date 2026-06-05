import json
import requests
import time

BASE_URL = "https://workflowhub.eu"

with open("galaxy_workflows_summary.json", "r") as f:
    galaxy_workflows = json.load(f)
    workflows = galaxy_workflows["data"]
    print(f"Found {len(workflows)} workflows in the Galaxy workflow hub.")

output_filename = "galaxy_workflows.jsonl"

with open(output_filename, "w") as f:
    for workflow in workflows:
        workflow_id = workflow["id"]
        url = f"{BASE_URL}/workflows/{workflow_id}.json"
        try:
            print(f"Fetching workflow {workflow_id} from {url}")

            response = requests.get(url, timeout=(10, 30))
            response.raise_for_status()

            # Append JSON content as new line in the output file
            json.dump(response.json(), f)
            f.write("\n")

            time.sleep(1)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching workflow {workflow_id}: {e}")

print(f"Finished writing workflow details to {output_filename}")

