import requests
import json
import time
from pathlib import Path

# According to site.json
# Total topics across all categories:
# use per_page=100 to reduce number of requests:
#     **Category**                **id**  **topic count**   **num reqs**
#     Uncategorized               1       2733                28
#     usegalaxy.org support       5       2030                21
#     usegalaxy.eu support        6       1303                14
#     Resources                   14      108                 2
#     usegalaxy.org.au support    10      82                  1
#     usegalaxy.be support        11      18                  1
#     Site Feedback               3       5                   1
#     News & Updates              15      3                   1
# Total: 6,282 topics, 69 requests


# Category ids based on site.json:
CATEGORY_IDS = [15, 3, 11, 10, 14, 6, 5, 1]

BASE_URL = "https://help.galaxyproject.org"
OUTPUT_DIR = Path("galaxy_topics")
OUTPUT_DIR.mkdir(exist_ok=True)


def fetch_category_topics(category_id, session, per_page=100):
    """Fetch all topics from a category, handling pagination."""
    all_topics = []
    page = 0

    while True:
        url = f"{BASE_URL}/c/{category_id}.json"
        params = {
            "page": page,
            "per_page": per_page,
            "no_definitions": "true"
        }
        
        try:
            response = session.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            topics = data.get("topic_list", {}).get("topics", [])
            if not topics:
                break
            
            all_topics.extend(topics)
            print(f"Category {category_id}: Collected {len(all_topics)} topics (page {page})")
            
            page += 1
            time.sleep(1)  # don't overload the server
            
        except Exception as e:
            print(f"Error fetching category {category_id}, page {page}: {e}")
            break
    
    return all_topics

def main():
    all_data = {}
    total_topics = 0
    
    with requests.Session() as session:
        for category_id in CATEGORY_IDS:
            print(f"\nFetching category {category_id}...")

            topics = fetch_category_topics(category_id, session=session)
            all_data[category_id] = topics
            total_topics += len(topics)
        
            # Save individual category file
            output_file = OUTPUT_DIR / f"category_{category_id}.json"
            with open(output_file, "w") as f:
                json.dump(topics, f, indent=2)

            print(f"Saved {len(topics)} topics to {output_file}")
    
    # Save combined data
    combined_file = OUTPUT_DIR / "all_topics.json"

    with open(combined_file, "w") as f:
        json.dump(all_data, f, indent=2)
    
    print(f"\nTotal topics collected: {total_topics}")
    print(f"Data saved to {OUTPUT_DIR}/")

if __name__ == "__main__":
    main()