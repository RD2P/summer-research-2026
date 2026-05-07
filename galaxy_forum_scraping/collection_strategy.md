# Galaxy Forum Topic Colection Strategy

## Intent: To gather data from galaxy forum and validate need for an agentic framework

Forum URL: https://help.galaxyproject.org/
The forum uses public Discourse endpoints (https://meta.discourse.org/)

Public endpoints available:
    - `https://help.galaxyproject.org/latest.json` - topic list (paginated)
    - `https://help.galaxyproject.org/t/{slug}/{id}.json` - full topic with all posts
    - `https://help.galaxyproject.org/site.json` - categories, tags, site metadata
    - `https://help.galaxyproject.org/about.json` - site stats, moderators, version
    - `https://help.galaxyproject.org/u/{username}.json` - public user profile

Paginate with:
    <url>?page=1

Change topics per page with:
    <url>?per_page=45

## Looking at site.json (https://help.galaxyproject.org/site.json):

Total topics across all categories: 
    
| Category                  | ID    | Topic count   |
|---                        |---:   |---:           |
| usegalaxy.org support     | 5     | 2030          |
| usegalaxy.eu support      | 6     | 1303          |
| usegalaxy.org.au support  | 10    | 82            |
| usegalaxy.be support      | 11    | 18            |
| Uncategorized             | 1     | 2733          |
| Site Feedback             | 3     | 5             |
| Resources                 | 14    | 108           |
| News & Updates            | 15    | 3             |

Total: 6,282 topics, 69 requests


## Data fetching strategy:
- Iterate over all categories by id
    <url>/c/<category_id>.json
- set per_page=100 (max)
    <url>/c/<category_id>.json?per_page=100
- iterate pages until topics is null

# Data format

- Per-category files:
  - Path: galaxy_topics/category_{category_id}.json
  - Format: JSON array of topic objects exactly as returned in topic_list.topics by the Discourse API (no post bodies fetched)
  - Example entry (one element of the array):
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
      "category_id": 6,
      // ...other fields returned by the API...
    }
    ```

- Combined file:
  - Path: galaxy_topics/all_topics.json
  - Format: JSON object mapping category_id → array of topic objects
  - Example:
    ```json
    {
      "6": [ { /* topic obj */ }, { /* topic obj */ } ],
      "5": [ { /* topic obj */ } ]
    }
    ```
