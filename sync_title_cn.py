import json

# Read both files
with open('docs/data/articles.json', 'r', encoding='utf-8') as f:
    docs_articles = json.load(f)

with open('marketing-intelligence/data/articles.json', 'r', encoding='utf-8') as f:
    mi_articles = json.load(f)

# Create lookup by URL from marketing-intelligence
title_cn_map = {}
for article in mi_articles:
    if 'title_cn' in article and article['title_cn']:
        key = article.get('url') or article.get('title')
        title_cn_map[key] = article['title_cn']

# Apply title_cn to docs articles
synced = 0
for article in docs_articles:
    key = article.get('url') or article.get('title')
    if key in title_cn_map:
        article['title_cn'] = title_cn_map[key]
        synced += 1

# Write back
with open('docs/data/articles.json', 'w', encoding='utf-8') as f:
    json.dump(docs_articles, f, ensure_ascii=False, indent=2)

print(f"Synced title_cn for {synced} articles to docs/data/articles.json")
