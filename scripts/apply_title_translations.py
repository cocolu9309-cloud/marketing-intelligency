import json
from pathlib import Path

# Apply title_translations.json to articles.json in both marketing-intelligence and docs
repo_root = Path(__file__).parent.parent
translations_path = repo_root / "title_translations.json"

if not translations_path.exists():
    print(f"[WARN] {translations_path} not found, skipping")
    exit(0)

translations = json.loads(translations_path.read_text(encoding="utf-8"))

for subpath in ["marketing-intelligence/data/articles.json", "docs/data/articles.json"]:
    articles_path = repo_root / subpath
    if not articles_path.exists():
        print(f"[WARN] {articles_path} not found, skipping")
        continue
    articles = json.loads(articles_path.read_text(encoding="utf-8"))
    applied = 0
    for a in articles:
        if a["url"] in translations and translations[a["url"]]:
            a["title_cn"] = translations[a["url"]]
            applied += 1
    articles_path.write_text(json.dumps(articles, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Applied {applied} translations to {subpath}")
