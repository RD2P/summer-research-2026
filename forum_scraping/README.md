# Forum Scraper

Tools to collect topic metadata and full post content from Discourse-based forums for downstream analysis.

## Purpose

This project gathers topic and post data from:

- **Galaxy** — https://help.galaxyproject.org/
- **Nextflow** — https://community.seqera.io/

The data is used to support analysis and validation of an agentic framework for scientific workflows.

## Data sources

Both forums expose public Discourse endpoints:

- `<base_url>/c/{id}.json` — category topics
- `<base_url>/t/{id}.json` — full topic with posts
- `<base_url>/site.json` — site metadata, categories, counts
- `<base_url>/about.json` — site stats, version, moderators
- `<base_url>/latest.json` — latest topics

## Query parameters

- `page` — pagination
- `per_page=100` — fetch up to 100 topics per request
- `no_definitions=true` — reduce payload where supported

---

## Forum summaries

### Galaxy

| Category | ID | Topic count | Post count | Category pages |
|---|---:|---:|---:|---:|
| usegalaxy.org support | 5 | 2030 | 8171 | 21 |
| usegalaxy.eu support | 6 | 1303 | 5570 | 14 |
| usegalaxy.org.au support | 10 | 82 | 314 | 1 |
| usegalaxy.be support | 11 | 18 | 62 | 1 |
| Uncategorized | 1 | 2733 | 10964 | 28 |
| Site Feedback | 3 | 5 | 24 | 1 |
| Resources | 14 | 108 | 457 | 2 |
| News & Updates | 15 | 3 | 4 | 1 |

**Totals**
- Topics: **6,282**
- Posts: **25,566**
- Category-page requests: **69**
- Topic-detail requests: **6,282**
- Total requests: **6,351**

### Nextflow

| Category | ID | Topic count | Post count | Category pages |
|---|---:|---:|---:|---:|
| Ask for help | 37 | 838 | 3540 | 9 |
| Training | 39 | 35 | 187 | 1 |
| Tips & Tricks | 36 | 28 | 55 | 1 |
| Events | 15 | 65 | 127 | 2 |
| Show & Tell | 43 | 3 | 5 | 1 |
| Announcements | 44 | 1 | 1 | 1 |
| Random | 4 | 1 | 4 | 1 |
| Uncategorized | 1 | 0 | 0 | 1 |

**Totals**
- Topics: **971**
- Posts: **3,919**
- Category-page requests: **17**
- Topic-detail requests: **971**
- Total requests: **988**

---

## Data fetching strategy

Current script flow in `main.py`:

1. **Fetch category topics**
   - Iterate through all category IDs for the selected forum
   - Fetch pages with:
     ```text
     <base_url>/c/<category_id>.json?page=<page>&per_page=100&no_definitions=true
     ```
   - Continue until no topics are returned

2. **Fetch full topic posts**
   - Load `all_topics.json`
   - For each topic, fetch:
     ```text
     <base_url>/t/<topic_id>.json
     ```
   - Save `post_stream.posts` for each topic

3. **Create final combined output**
   - Load `all_topics.json`
   - Load `all_posts.json`
   - Join by topic ID
   - Extract `cooked` from the first post
   - Write `final_output.json`

4. **Verification**
   - Validate each topic record has:
     - `id`
     - `title`
     - `category_id`
     - `posts`
   - Validate each post has:
     - `id`
     - `cooked`

## Output files

### `all_topics.json`
Flat array of topic metadata returned from category endpoints.

Example:
```json
{
  "id": 12345,
  "title": "Example topic title",
  "created_at": "2024-01-02T03:04:05.000Z",
  "posts_count": 4,
  "reply_count": 3,
  "highest_post_number": 4,
  "last_posted_at": "2024-05-07T12:34:56.000Z",
  "views": 256,
  "category_id": 37
}
```

### `all_posts.json`
JSON array of topic records with full posts.

Example:
```json
{
  "id": 12345,
  "title": "Example topic title",
  "category_id": 37,
  "posts": [
    {
      "id": 111,
      "username": "user1",
      "created_at": "2024-01-02T03:04:05.000Z",
      "cooked": "<p>First post body</p>"
    },
    {
      "id": 112,
      "username": "user2",
      "created_at": "2024-01-02T04:10:00.000Z",
      "cooked": "<p>Reply body</p>"
    }
  ]
}
```

### `final_output.json`
Combined flat dataset with one record per topic.

Desired final format:
```json
[
  {
    "id": 1,
    "title": "Sample Topic",
    "cooked": "<p>This is a sample topic.</p>",
    "created_at": "2023-01-01T00:00:00Z",
    "posts_count": 5,
    "reply_count": 4,
    "highest_post_number": 5,
    "last_posted_at": "2023-01-01T00:00:00Z",
    "liked": false,
    "views": 10,
    "like_count": 2,
    "has_accepted_answer": false,
    "category_id": 37,
    "tags": ["nextflow", "tutorial"]
  }
]
```

### `all_replies.json`
Derived dataset containing only replies for each topic.

Example:
```json
[
  {
    "topic_id": 12345,
    "title": "Example topic title",
    "post_id": 111,
    "replies": [
      {
        "id": 112,
        "cooked": "<p>Reply body</p>",
        "created_at": "2024-01-02T04:10:00.000Z"
      },
      {
        "id": 113,
        "cooked": "<p>Another reply</p>",
        "created_at": "2024-01-02T05:15:00.000Z"
      }
    ]
  }
]
```

Notes:
- `post_id` is the first post in the topic.
- `replies` contains all posts after the first post.
- Each reply stores only `id`, `cooked`, and `created_at`.

## Notes

- The script uses a delay between category page requests.
- `FORUM_KEY` in `main.py` controls whether Galaxy or Nextflow is scraped.
- Outputs are written under the selected forum’s results directory.
- `per_page=100` is used to reduce the number of requests.