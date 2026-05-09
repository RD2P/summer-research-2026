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


def create_final_output():
    """
    Create final output combining topics and posts with all desired fields.
    
     1. Load all topics from OUTPUT_DIR/all_topics.json
     2. Load all posts from OUTPUT_DIR/all_posts.json
     3. For each topic, find the corresponding posts and extract the cooked content of the first post
     4. Create a new record with the required fields and save to OUTPUT_DIR/final_output.json
    """
    
    all_topics_file = OUTPUT_DIR / "all_topics.json"
    all_posts_file = OUTPUT_DIR / "all_posts.json"
    output_file = OUTPUT_DIR / "final_output.json"
    
    # Load all topics and posts
    with open(all_topics_file, "r") as f:
        all_topics = json.load(f)
    
    with open(all_posts_file, "r") as f:
        all_posts = json.load(f)
    
    # Create a lookup map for posts by topic_id
    posts_by_topic_id = {post["id"]: post for post in all_posts}
    
    # Create final records
    final_records = []
    
    for topic in all_topics:
        topic_id = topic.get("id")
        posts = posts_by_topic_id.get(topic_id, {}).get("posts", [])
        
        # Get cooked content from first post
        cooked = posts[0].get("cooked", "") if posts else ""
        
        # Extract tag names
        tags = [tag.get("name") for tag in topic.get("tags", [])] if topic.get("tags") else []
        
        record = {
            "id": topic.get("id"),
            "title": topic.get("title"),
            "cooked": cooked,
            "created_at": topic.get("created_at"),
            "posts_count": topic.get("posts_count"),
            "reply_count": topic.get("reply_count"),
            "highest_post_number": topic.get("highest_post_number"),
            "last_posted_at": topic.get("last_posted_at"),
            "liked": topic.get("liked"),
            "views": topic.get("views"),
            "like_count": topic.get("like_count"),
            "has_accepted_answer": topic.get("has_accepted_answer"),
            "category_id": topic.get("category_id"),
            "tags": tags,
        }
        
        final_records.append(record)
    
    # Save to file
    with open(output_file, "w") as f:
        json.dump(final_records, f, indent=2, ensure_ascii=False)
    
    print(f"Created final output with {len(final_records)} topics")
    print(f"Data saved to {output_file}")


def create_all_replies():
    """
    Create all_replies.json from all_posts.json.

    Output format:
    [
      {
        "id": <topic_id>,
        "title": <topic_title>,
        "post_id": <first_post_id>,
        "replies": [
          {"id": ..., "cooked": ..., "created_at": ...},
          ...
        ]
      }
    ]
    """
    all_posts_file = OUTPUT_DIR / "all_posts.json"
    output_file = OUTPUT_DIR / "all_replies.json"

    with open(all_posts_file, "r") as f:
        topics = json.load(f)

    all_replies = []

    for topic in topics:
        posts = topic.get("posts", [])
        if not posts:
            continue

        first_post = posts[0]
        replies = [
            {
                "id": post.get("id"),
                "cooked": post.get("cooked", ""),
                "created_at": post.get("created_at"),
            }
            for post in posts[1:]
        ]

        all_replies.append({
            "topic_id": topic.get("id"),
            "title": topic.get("title"),
            "post_id": first_post.get("id"),
            "replies": replies,
        })

    with open(output_file, "w") as f:
        json.dump(all_replies, f, indent=2, ensure_ascii=False)

    print(f"Saved replies for {len(all_replies)} topics to {output_file}")


if __name__ == "__main__":

    # 1. fetch topics by category
    # fetch_category_topics()

    # 2. fetch posts for all topics (todo)
    # fetch_all_topic_posts()

    # 3. verify all_posts.json has the required fields
    # verify_all_posts()

    # 4. create final output with desired fields for all topics
    # create_final_output()

    # 5. create output with all replies for each topic
    # create_all_replies()

    pass