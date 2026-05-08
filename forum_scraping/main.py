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

# ============================== #
# === choose forum to scrape === #
# ============================== #

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


def fetch_all_topic_posts():
    """
    Fetch post_stream.posts for every topic in all_topics.json and save to all_posts.json.
    1. Iterate over all topics in OUTPUT_DIR/all_topics.json 
    2. Fetch info for each topic from BASE_URL/t/{id}.json
    3. Save the posts for each topic in OUTPUT_DIR/all_posts.json    
    """
    
    all_topics_file = OUTPUT_DIR / "all_topics.json"
    all_posts_file = OUTPUT_DIR / "all_posts.json"

    with open(all_topics_file, "r") as f:
        topics = json.load(f)

    with requests.Session() as session, open(all_posts_file, "w") as out:
        out.write("[\n")  # start of JSON array
        first = True

        post_count = 0

        for i, topic in enumerate(topics, start=1):
            topic_id = topic.get("id")
            if not topic_id:
                continue

            try:
                url = f"{BASE_URL}/t/{topic_id}.json"
                response = session.get(url, timeout=30)
                response.raise_for_status()
                data = response.json()

                posts = data.get("post_stream", {}).get("posts", [])

                record = {
                    "id": topic_id,
                    "title": topic.get("title"),
                    "category_id": topic.get("category_id"),
                    "posts": posts
                }

                if not first:
                    out.write(",\n")  # comma between records

                json.dump(record, out, indent=2, ensure_ascii=False)
                first = False
                post_count += 1

                print(f"[{i}/{len(topics)}] Fetched {len(posts)} posts for topic {topic_id}")
                time.sleep(0.3)

            except Exception as e:
                print(f"Error fetching topic {topic_id}: {e}")

        out.write("\n]")  # end of JSON array

    print(f"\nSaved posts for {post_count} topics to {all_posts_file}")


# ============================= #
# === Verify all_posts.json === #
# ============================= #


def verify_all_posts():
    """Verify that all_posts.json has the required fields for each topic and post."""
    with open(OUTPUT_DIR / "all_posts.json", "r") as f:
        posts_data = json.load(f)

    for post in posts_data:
        assert("posts" in post), f"Missing 'posts' key in topic {post.get('id')}"
        assert("id" in post), f"Missing 'id' key in topic {post}"
        assert("title" in post), f"Missing 'title' key in topic {post.get('id')}"
        assert("category_id" in post), f"Missing 'category_id' key in topic {post.get('id')}"
        for p in post["posts"]:
            assert("id" in p), f"Missing 'id' key in post of topic {post.get('id')}"
            assert("username" in p), f"Missing 'username' key in post of topic {post.get('id')}"
            assert("created_at" in p), f"Missing 'created_at' key in post of topic {post.get('id')}"
            assert("cooked" in p), f"Missing 'cooked' key in post of topic {post.get('id')}"

    print(f"Verified {len(posts_data)} topics have required fields and posts.")


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

    # 1. fetch topics by category
    # fetch_category_topics()

    # 2. fetch posts for all topics (todo)
    # fetch_all_topic_posts()

    # 3. verify all_posts.json has the required fields
    # verify_all_posts()

    # 4. create final output with desired fields for all topics
    # parse_topics_flat()

    pass