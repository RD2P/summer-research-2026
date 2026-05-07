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
| News & Updates            | 15    | 4             |
|                           |       |               |

## Data fetching strategy:
- Iterate over all categories by id
    <url>/c/<category_id>.json
- set per_page=100 (max)
    <url>/c/<category_id>.json?per_page=100
- iterate pages until topics is null

## Questions
- exactly what data in what format do we need?