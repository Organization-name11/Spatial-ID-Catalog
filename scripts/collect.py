import requests
import json
import os
import sys
import base64
from time import sleep

# 保存先ディレクトリ作成
os.makedirs("docs/data", exist_ok=True)

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    print("Error: GITHUB_TOKEN is not set")
    sys.exit(1)

API_URL = "https://api.github.com/search/repositories"

# 検索クエリ：README・概要・トピック・リポジトリ名にキーワードを含むもの
QUERY = (
    '"空間ID" OR "空間ＩＤ" OR "spatialid" OR "ＳＰＡＴＩＡＬＩＤ" OR '
    '"spatial-id" OR "ＳＰＡＴＩＡＬーＩＤ" in:description,topics,name'
)

HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}"
}

PARAMS = {
    "q": QUERY,
    "per_page": 100,  # 1ページあたり最大100件
    "page": 1,
    "sort": "updated",
    "order": "desc"
}

# ページング対応
all_items = []
while True:
    res = requests.get(API_URL, headers=HEADERS, params=PARAMS)
    if res.status_code != 200:
        print(res.text)
        sys.exit(1)

    data = res.json()
    items = data.get("items", [])
    if not items:
        break

    all_items.extend(items)

    # 最大 4ページまで取得（100件 × 4ページ = 400件）
    if PARAMS["page"] >= 4 or len(items) < 100:
        break
    PARAMS["page"] += 1
    sleep(1)  # GitHub API rate limit 回避のため少し待機

print(f"Found {len(all_items)} repositories from search API")

# README を取得してキーワードチェック
KEYWORDS = ["空間ID", "空間ＩＤ", "spatialid", "ＳＰＡＴＩＡＬＩＤ", "spatial-id", "ＳＰＡＴＩＡＬーＩＤ"]

catalog = []

for repo in all_items:
    full_name = repo["full_name"]
    readme_url = f"https://api.github.com/repos/{full_name}/readme"

    try:
        r = requests.get(readme_url, headers=HEADERS)
        if r.status_code == 200:
            readme_data = r.json()
            content = base64.b64decode(readme_data["content"]).decode("utf-8", errors="ignore")
        else:
            content = ""
    except Exception as e:
        print(f"Error fetching README for {full_name}: {e}")
        content = ""

    # README にキーワードが含まれるか
    if any(k in content for k in KEYWORDS) or repo["name"] in KEYWORDS:
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

print(f"Collected {len(catalog)} repositories containing keywords")
