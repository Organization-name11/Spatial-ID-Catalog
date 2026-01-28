import requests
import json
import os
import sys

# 保存先ディレクトリ作成
os.makedirs("docs/data", exist_ok=True)

API_URL = "https://api.github.com/search/repositories"

# 検索クエリ：README・概要・トピック・リポジトリ名にキーワードを含むもの
QUERY = (
    '"空間ID" OR "空間ＩＤ" OR "spatialid" OR "ＳＰＡＴＩＡＬＩＤ" OR '
    '"spatial-id" OR "ＳＰＡＴＩＡＬーＩＤ" in:readme,description,topics,name'
)

HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {os.environ.get('GITHUB_TOKEN', '')}"
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
        "topics": repo.get("topics", []),
        "license": repo["license"],
        "fork": repo["fork"],
        "open_issues_count": repo["open_issues_count"],
        "watchers_count": repo["watchers_count"],
        "forks_count": repo["forks_count"]
    })

with open("docs/data/catalog.json", "w", encoding="utf-8") as f:
    json.dump(catalog, f, indent=2, ensure_ascii=False)

print(f"Collected {len(catalog)} repositories")
