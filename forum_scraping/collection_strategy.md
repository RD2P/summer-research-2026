# Forum Topic Collection Strategy

## Intent: To gather data from Galaxy and Nextflow forums and validate need for an agentic framework

### Forum URLs:
- Galaxy: https://help.galaxyproject.org/
- Nextflow: https://community.seqera.io/

Both forums use public Discourse endpoints (https://meta.discourse.org/)

### Public endpoints available:
- `<base_url>/latest.json` - topic list (paginated)
- `<base_url>/c/{id}.json` - full category
- `<base_url>/t/{id}.json` - full topic with all posts
- `<base_url>/site.json` - categories, tags, site metadata
- `<base_url>/about.json` - site stats, moderators, version
- `<base_url>/u/{username}.json` - public user profile

### Query parameters:
- Paginate: `?page=1`
- Topics per page: `?per_page=100`
- Reduce payload: `?no_definitions=true`

---

## Galaxy Forum

### Category breakdown (from site.json):

| Category                  | ID    | Topic count   | Post count |
|---                        |---:   |---:           |---:        |
| usegalaxy.org support     | 5     | 2030          | 8171       |
| usegalaxy.eu support      | 6     | 1303          | 5570       |
| usegalaxy.org.au support  | 10    | 82            | 314        |
| usegalaxy.be support      | 11    | 18            | 62         |
| Uncategorized             | 1     | 2733          | 10964      |
| Site Feedback             | 3     | 5             | 24         |
| Resources                 | 14    | 108           | 457        |
| News & Updates            | 15    | 3             | 4          |

**Total: 6,282 topics, ~69 requests @ per_page=100**

---

## Nextflow Forum

### Category breakdown (from site.json):

| Category                  | ID    | Topic count   | Post count |
|---                        |---:   |---:           |---:        |
| Ask for help              | 37    | 838           | 3540       |
| Training                  | 39    | 35            | 187        |
| Tips & Tricks             | 36    | 28            | 55         |
| Events                    | 15    | 65            | 127        |
| Show & Tell               | 43    | 3             | 5          |
| Announcements             | 44    | 1             | 1          |
| Random                    | 4     | 1             | 4          |
| Uncategorized             | 1     | 0             | 0          |

**Total: 971 topics, ~10 requests @ per_page=100**

---

## Data fetching strategy

1. Iterate over all categories by ID
   ```
   <base_url>/c/<category_id>.json?per_page=100&no_definitions=true
   ```

2. Paginate through results until `topics` array is empty

3. Add 1 second delay between requests (rate limiting)

4. Save per-category and combined flat files

---

## Data format

### Per-category files:
- Path: `{forum}_results/category_{category_id}.json`
  - Example: `galaxy_results/category_5.json`, `nextflow_results/category_37.json`
- Format: JSON array of topic objects as returned by `/c/{id}.json`
- Example entry:
  ```json
  {
    "id": 12345,
    "title": "Example topic title",
    "slug": "example-topic-title",
    "created_at": "2024-01-02T03:04:05.000Z",
    "last_posted_at": "2024-05-07T12:34:56.000Z",
    "posts_count": 4,
    "views": 256,
    "reply_count": 3,
    "highest_post_number": 4,
    "excerpt": "Short HTML/text excerpt",
    "category_id": 5
  }
  ```

### Combined flat file:
- Path: `{forum}_results/all_topics.jsonl`
  - Example: `galaxy_results/all_topics.jsonl`, `nextflow_results/all_topics.jsonl`
- Format: **JSONL** (one JSON topic object per line)
- Streaming-friendly format to avoid high memory usage
- Each line is a valid JSON object with `category_id` included
- Example:
  ```
  {"id":12345,"title":"Example topic title","posts_count":4,"reply_count":3,"created_at":"2024-01-02T03:04:05.000Z","category_id":5}
  {"id":12346,"title":"Another topic","posts_count":2,"reply_count":1,"created_at":"2024-01-03T10:20:30.000Z","category_id":5}
  ```
