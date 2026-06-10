# -*- coding: utf-8 -*-
import json
import os
from pathlib import Path
import requests

API_KEY = "sk-natrqylrddzmxhsnqxfmuiuvslcuhgrfxjlqmlticqepotmp"
API_URL = "https://api.siliconflow.cn/v1/chat/completions"

def call_llm(prompt, model="deepseek-ai/DeepSeek-V3"):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500,
        "temperature": 0.7
    }
    resp = requests.post(API_URL, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"].strip()

def process_article(article):
    title = article.get("title", "")
    content_type = article.get("content_type", "其他")
    department = article.get("department", "品牌")
    url = article.get("url", "")
    source = article.get("source", "")
    source_name = article.get("source_name", source)
    importance = article.get("importance", "中")
    published = article.get("published", "")
    crawled_at = article.get("crawled_at", "")

    prompt = f"""你是一个专业的跨境电商营销顾问。请根据以下文章信息，生成中文摘要。

文章标题（英文）：{title}
来源：{source_name}
类型：{content_type}
部门：{department}

请按以下格式生成摘要（每项1-2句话）：

【中文标题】<将英文标题翻译成中文，简洁准确，不超过30字>
【一句话结论】<用1句话概括文章核心内容，不超过30字>
【为什么重要】<用1句话说明为什么营销人员需要关注这个内容，结合callie.com定制礼品跨境电商的背景，20-40字>
【可以怎么用】<用1句话说明如何将这个内容应用到callie.com的实际营销工作中，30-50字>

只输出这4项，不要其他内容。"""

    try:
        result = call_llm(prompt)
        lines = result.split("\n")
        cn_title = ""
        one_sentence = ""
        why_important = ""
        how_to_use = ""

        for line in lines:
            line = line.strip()
            if line.startswith("【中文标题】"):
                cn_title = line.replace("【中文标题】", "").strip()
            elif line.startswith("【一句话结论】"):
                one_sentence = line.replace("【一句话结论】", "").strip()
            elif line.startswith("【为什么重要】"):
                why_important = line.replace("【为什么重要】", "").strip()
            elif line.startswith("【可以怎么用】"):
                how_to_use = line.replace("【可以怎么用】", "").strip()

        if not cn_title:
            cn_title = title[:30] + "..." if len(title) > 30 else title
        if not one_sentence:
            one_sentence = cn_title

        return {
            "title": title,
            "title_cn": cn_title,
            "source": source,
            "source_name": source_name,
            "department": department,
            "content_type": content_type,
            "importance": importance,
            "url": url,
            "published": published,
            "crawled_at": crawled_at,
            "one_sentence": one_sentence,
            "why_important": why_important,
            "how_to_use": how_to_use
        }
    except Exception as e:
        print(f"  [ERROR] Failed to process: {title[:30]}... - {e}")
        return {
            "title": title,
            "title_cn": title[:30],
            "source": source,
            "source_name": source_name,
            "department": department,
            "content_type": content_type,
            "importance": importance,
            "url": url,
            "published": published,
            "crawled_at": crawled_at,
            "one_sentence": title[:30],
            "why_important": f"来自{source_name}的营销资讯",
            "how_to_use": "评估后决定是否试点应用"
        }

def main():
    input_path = Path("data/articles.json")
    if not input_path.exists():
        print(f"[ERROR] File not found: {input_path}")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        articles = json.load(f)

    print(f"[INFO] Processing {len(articles)} articles...")
    new_articles = []
    for i, article in enumerate(articles):
        title_short = article.get('title', '')[:30]
        print(f"  [{i+1}/{len(articles)}] Processing: {title_short}...")
        new_article = process_article(article)
        new_articles.append(new_article)

    with open(input_path, "w", encoding="utf-8") as f:
        json.dump(new_articles, f, ensure_ascii=False, indent=2)

    print(f"[DONE] Updated {len(new_articles)} articles in {input_path}")

if __name__ == "__main__":
    main()