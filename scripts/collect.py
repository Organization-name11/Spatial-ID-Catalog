import requests
import json
import os
import sys

API_URL = "https://api.github.com/search/repositories"

QUERY = (
    '"空間ID" OR "空間ＩＤ" OR "spatialid" OR "spatial-id" '
    'in:readme,description,topics'
)

HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"
}

PARAMS = {
    "q": QUERY,
    "per_page": 30,
    "sort": "updated",
    "order": "desc"
}

res = requests.get(API_URL, headers=HEADERS, params=PARAMS)
if res.status_code != 200:
    print(res.text)
    sys.exit(1)

items = res.json().get("items", [])

catalog = []
for repo in items:
    catalog.append({
        "name": repo["name"],
        "full_name": repo["full_name"],
        "url": repo["html_url"],
        "description": repo["description"],
        "language": repo["language"],
        "stars": repo["stargazers_count"],
        "updated_at": repo["updated_at"],
        "topics": repo.get("topics", [])
    })

with open("data/catalog.json", "w", encoding="utf-8") as f:
    json.dump(catalog, f, indent=2, ensure_ascii=False)

print(f"Collected {len(catalog)} repositories")
