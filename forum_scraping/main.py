import requests
import json
import time
from pathlib import Path

# === define constant vals based on forum === #

FORUMS =  {
    "galaxy": {
        "base_url": "https://help.galaxyproject.org",
        "category_ids": [15, 3, 11, 10, 14, 6, 5, 1],
        "output_dir": Path("galaxy_results")
    },
    "nextflow": {
        "base_url": "https://community.seqera.io",
        "category_ids": [37, 39, 36, 15, 43, 44, 4, 1],
        "output_dir": Path("nextflow_results")
    }
}

# === choose forum to scrape === #

# "galaxy" or "nextflow"
FORUM_KEY = "nextflow" 

BASE_URL = FORUMS[FORUM_KEY]["base_url"]
CATEGORY_IDS = FORUMS[FORUM_KEY]["category_ids"]
OUTPUT_DIR = FORUMS[FORUM_KEY]["output_dir"]
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ================================ #
# === Fetch topics by category === #
# ================================ #

def _fetch_category_topics(category_id, session, per_page=100):
    """Fetch all topics from a category, handling pagination."""
    category_topics = []
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
            
            category_topics.extend(topics)
            print(f"Category {category_id}: Collected {len(topics)} topics (page {page})")
            
            page += 1
            time.sleep(1)  # don't overload the server
            
        except Exception as e:
            print(f"Error fetching category {category_id}, page {page}: {e}")
            break
    
    return category_topics

def fetch_category_topics():
    all_topics = []
    total_topics = 0

    # file to save combined data
    combined_file = OUTPUT_DIR / "all_topics.json"
    
    with requests.Session() as session:
        for category_id in CATEGORY_IDS:
            print(f"\nFetching category {category_id}...")

            topics = _fetch_category_topics(category_id, session=session)
            total_topics += len(topics)

            print(f"Fetched {len(topics)} topics from category {category_id}. Total so far: {total_topics}")

            all_topics.extend(topics)

    with open(combined_file, "w") as f:
        json.dump(all_topics, f, indent=2)
    
    print(f"\nTotal topics collected: {total_topics}")
    print(f"Data saved to {OUTPUT_DIR}/")


# ================================== #
# === Fetch posts for all topics === #
# ================================== #
# todo

# =========================== #
# === Create final output === #
# =========================== #

def parse_topics_flat():
    """Parse all_topics.json and extract minimal fields into topics_flat.json"""
    
    # Load all topics
    all_topics_file = OUTPUT_DIR / "all_topics.json"
    with open(all_topics_file, "r") as f:
        topics = json.load(f)
    
    # extract fields
    flat_topics = []
    for topic in topics:
        flat_topics.append({
            "id": topic.get("id"),
            "title": topic.get("title"),
            "posts_count": topic.get("posts_count"),
            "reply_count": topic.get("reply_count"),
            "created_at": topic.get("created_at"),
            "category_id": topic.get("category_id"),
        })
    
    # Save flat file
    flat_file = OUTPUT_DIR / "topics_flat.json"
    with open(flat_file, "w") as f:
        json.dump(flat_topics, f, indent=2)
    
    print(f"Saved {len(flat_topics)} flattened topics to {flat_file}")

if __name__ == "__main__":

    # fetch topics by category
    fetch_category_topics()

    # fetch posts for all topics (todo)
    # fetch_all_topic_posts

    # create final output with desired fields for all topics
    # parse_topics_flat()