# Forum Topic Collection Strategy

## Intent
Gather topic and post data from Galaxy and Nextflow forums to support analysis and validate the need for an agentic framework for scientific workflows.

## Forums
- Galaxy: https://help.galaxyproject.org/
- Nextflow: https://community.seqera.io/

Both forums use public Discourse endpoints.

## Public endpoints
- `<base_url>/c/{id}.json` — category topics
- `<base_url>/t/{id}.json` — full topic with posts
- `<base_url>/site.json` — site metadata, categories, counts
- `<base_url>/about.json` — site stats, version, moderators
- `<base_url>/latest.json` — latest topics

## Query parameters
- `page` — pagination
- `per_page=100` — fetch up to 100 topics per page
- `no_definitions=true` — reduce payload where supported

---

## Galaxy forum

### Category breakdown

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
- Requests for category pages: **69**
- Topic detail requests: **6,282**
- Total requests: **6,351**

---

## Nextflow forum

### Category breakdown

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
- Requests for category pages: **17**
- Topic detail requests: **971**
- Total requests: **988**

---

## Data fetching strategy

Current script flow in `main.py`:

1. **Fetch category topics**
   - Iterate through all category IDs
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
   - Validate that each topic record has:
     - `id`
     - `title`
     - `category_id`
     - `posts`
   - Validate each post has:
     - `id`
     - `username`
     - `created_at`
     - `cooked`

---

## Output files

### 1) `all_topics.json`
Flat array of topic metadata returned from category endpoints.

Example record:
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

### 2) `all_posts.json`
JSON array of topic records with full posts.

Example record:
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

### 3) `final_output.json`
Combined flat dataset with one record per topic.

Example record:
```json
{
  "id": 12345,
  "title": "Example topic title",
  "cooked": "<p>First post body</p>",
  "created_at": "2024-01-02T03:04:05.000Z",
  "posts_count": 4,
  "reply_count": 3,
  "highest_post_number": 4,
  "last_posted_at": "2024-05-07T12:34:56.000Z",
  "liked": false,
  "views": 256,
  "like_count": 2,
  "has_accepted_answer": false,
  "category_id": 37,
  "tags": ["nextflow", "tutorial"]
}
```

---

## Notes
- The script uses a 1 second delay between category page requests.
- The topic fetch step is the main source of request volume.
- Outputs are written under the selected forum’s results directory.
- `FORUM_KEY` in `main.py` controls whether Galaxy or Nextflow is scraped.