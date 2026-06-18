import json
from pathlib import Path

# Build title_translations.json from marketing-intelligence/data/articles.json
repo_root = Path(__file__).parent.parent
articles = json.loads((repo_root / "marketing-intelligence" / "data" / "articles.json").read_text(encoding="utf-8"))
translations = {}
for a in articles:
    if a.get("title_cn"):
        translations[a["url"]] = a["title_cn"]

output_path = repo_root / "title_translations.json"
output_path.write_text(
    json.dumps(translations, ensure_ascii=False, indent=2),
    encoding="utf-8"
)
print(f"Saved {len(translations)} translations to {output_path}")
