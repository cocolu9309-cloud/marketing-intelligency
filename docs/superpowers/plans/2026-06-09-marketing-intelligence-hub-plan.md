# Marketing Intelligence Hub Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 搭建一个全自动化的营销资讯静态网页，支持搜索和筛选，通过钉钉链接分享访问

**Architecture:** Python 爬虫每日抓取 RSS 和竞品网站 → 生成 JSON 数据 → Hugo 生成静态网页 → GitHub Pages 托管 →每天自动更新

**Tech Stack:** Python + feedparser/requests/beautifulsoup4 | Hugo | GitHub Pages | GitHub Actions

---

## File Structure

```
marketing-intelligence/
├── README.md
├── config.toml                        # Hugo 配置
├── data/
│   └── .gitkeep # JSON 数据由爬虫生成，不提交到 git
├── scripts/
│   └── crawl.py                      # Python 爬虫主脚本
├── src/
│   ├── index.html                    # 首页 HTML
│   ├── css/
│   │   └── style.css                # 样式文件
│   └── js/
│       └── search.js                # 搜索筛选逻辑
├── layouts/
│   └── index.html                   # Hugo 列表页模板
└── .github/
    └── workflows/
        └── daily-crawl-deploy.yml   # GitHub Actions 工作流
```

---

## Task 1: 创建项目目录结构

**Files:**
- Create: `marketing-intelligence/scripts/`
- Create: `marketing-intelligence/data/`
- Create: `marketing-intelligence/src/css/`
- Create: `marketing-intelligence/src/js/`
- Create: `marketing-intelligence/layouts/`
- Create: `marketing-intelligence/.github/workflows/`
- Create: `marketing-intelligence/data/.gitkeep`

- [ ] **Step 1: 创建目录结构**

```powershell
New-Item -ItemType Directory -Force marketing-intelligence/scripts
New-Item -ItemType Directory -Force marketing-intelligence/data
New-Item -ItemType Directory -Force marketing-intelligence/src/css
New-Item -ItemType Directory -Force marketing-intelligence/src/js
New-Item -ItemType Directory -Force marketing-intelligence/layouts
New-Item -ItemType Directory -Force marketing-intelligence/.github/workflows
New-Item -ItemType File -Path marketing-intelligence/data/.gitkeep
```

- [ ] **Step 2: Commit**

```bash
git add marketing-intelligence/
git commit -m "feat: create project directory structure"
```

---

## Task 2: 编写 Python 爬虫脚本

**Files:**
- Create: `marketing-intelligence/scripts/crawl.py`

**Dependencies:**
- `feedparser` —解析 RSS
- `requests` — 发送 HTTP 请求
- `beautifulsoup4` — 解析 HTML
- `html2text` — 把 HTML 转成纯文本（用于摘要）

**RSS Sources（直接可用）:**

```python
RSS_SOURCES = {
    "adweek": "https://www.adweek.com/feed/",
    "marketing_week": "https://www.marketingweek.com/feed/",
    "social_media_today": "https://www.socialmediatoday.com/rss.xml",
    "search_engine_journal": "https://www.searchenginejournal.com/feed/",
    "tiktok_business": "https://business.tiktok.com/blog/rss",
    "youtube_blog": "https://blog.youtube/rss.xml",
    "google_ads_blog": "https://adsdeveloper.blogspot.com/feeds/posts/default",
    "meta_business": "https://www.facebook.com/business/news/rss",
}
```

**竞品 Websites（需要爬取）:**

```python
COMPETITOR_SITES = [
    {"name": "wanderprints", "url": "https://www.etsy.com/shop/wanderprints"},
    {"name": "macorner", "url": "https://www.etsy.com/shop/macorner"},
    {"name": "pawsionate", "url": "https://www.etsy.com/shop/pawsionate"},
]
```

**数据字段映射（部门归属）:**

```python
DEPARTMENT_MAPPING = {
    "search_engine_journal": "SEO",
    "adweek": "品牌",
    "marketing_week": "品牌",
    "social_media_today": "社媒运营",
    "tiktok_business": "社媒运营",
    "youtube_blog": "社媒运营",
    "google_ads_blog": "广告投放",
    "meta_business": "广告投放",
}
```

- [ ] **Step 1: 写爬虫脚本**

```python
#!/usr/bin/env python3
"""
营销资讯爬虫脚本
每天抓取 RSS 源和竞品网站，生成 data/articles.json
"""

import json
import re
import time
from datetime import datetime
from pathlib import Path

import feedparser
import requests
from bs4 import BeautifulSoup

# ========== 配置 ==========

RSS_SOURCES = {
    "adweek": "https://www.adweek.com/feed/",
    "marketing_week": "https://www.marketingweek.com/feed/",
    "social_media_today": "https://www.socialmediatoday.com/rss.xml",
    "search_engine_journal": "https://www.searchenginejournal.com/feed/",
    "tiktok_business": "https://business.tiktok.com/blog/rss",
    "youtube_blog": "https://blog.youtube/rss.xml",
    "google_ads_blog": "https://adsdeveloper.blogspot.com/feeds/posts/default",
    "meta_business": "https://www.facebook.com/business/news/rss",
}

COMPETITOR_SITES = [
    {"name": "wanderprints", "url": "https://www.etsy.com/shop/wanderprints"},
    {"name": "macorner", "url": "https://www.etsy.com/shop/macorner"},
    {"name": "pawsionate", "url": "https://www.etsy.com/shop/pawsionate"},
]

DEPARTMENT_MAPPING = {
    "search_engine_journal": "SEO",
    "adweek": "品牌",
    "marketing_week": "品牌",
    "social_media_today": "社媒运营",
    "tiktok_business": "社媒运营",
    "youtube_blog": "社媒运营",
    "google_ads_blog": "广告投放",
    "meta_business": "广告投放",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# ========== 工具函数 ==========

def generate_summary(title, content, content_type, department):
    """根据标题和内容生成三段式摘要"""
    # 一句话结论：直接用标题的前30字
    conclusion = title[:30] + "..." if len(title) > 30 else title

    # 为什么重要：根据内容类型生成
    why_important_map = {
        "新玩法": "代表行业新趋势，可能影响现有营销策略",
        "数据报告": "提供最新行业数据和benchmark参考",
        "工具推荐": "可能提升团队工作效率",
        "案例分享": "实战经验，可供借鉴和复用到callie.com",
        "平台更新": "平台功能变化，需及时了解并调整策略",
    }
    why_important = why_important_map.get(content_type, "行业动态更新")

    # 可以怎么用：根据部门归属生成
    how_to_use_map = {
        "SEO": "评估对SEO策略的影响，考虑在下次优化中应用",
        "社媒运营": "评估对社媒运营策略的影响，考虑试点新功能",
        "广告投放": "评估对广告投放策略的影响，考虑调整预算分配",
        "红人营销": "评估对红人合作策略的影响，考虑试点新合作模式",
        "用户运营": "评估对用户运营策略的影响，考虑优化用户旅程",
        "品牌": "评估对品牌营销策略的影响，考虑融入品牌传播计划",
    }
    how_to_use = how_to_use_map.get(department, "评估后决定是否试点")

    return {
        "一句话结论": conclusion,
        "为什么重要": why_important,
        "可以怎么用": how_to_use,
    }


def determine_content_type(entry):
    """根据标题和内容关键词判断内容类型"""
    title_lower = entry.get("title", "").lower()
    summary_lower = entry.get("summary", "").lower()

    text = title_lower + " " + summary_lower

    if any(k in text for k in ["new feature", "launch", "update", "announce"]):
        return "平台更新"
    if any(k in text for k in ["case study", "success story", "how to"]):
        return "案例分享"
    if any(k in text for k in ["tool", "app", "software", "platform"]):
        return "工具推荐"
    if any(k in text for k in ["report", "data", "study", "research", "statistic"]):
        return "数据报告"
    return "新玩法"


def determine_importance(entry):
    """根据内容判断重要程度"""
    title_lower = entry.get("title", "").lower()
    summary_lower = entry.get("summary", "").lower()
    text = title_lower + " " + summary_lower

    # 包含重大关键词的为必读
    critical_keywords = ["breaking", "urgent", "important", "must know", "critical update"]
    if any(k in text for k in critical_keywords):
        return "⭐⭐⭐"

    # 平台官方博客和一级来源为推荐
    return "⭐⭐"


def parse_rss_source(source_key, url):
    """解析单个 RSS 源"""
    articles = []
    try:
        feed = feedparser.parse(url)
        department = DEPARTMENT_MAPPING.get(source_key, "品牌")

        for entry in feed.entries[:20]:  # 每次最多取20条
            content_type = determine_content_type(entry)
            importance = determine_importance(entry)
            summary = generate_summary(
                entry.get("title", ""),
                entry.get("summary", ""),
                content_type,
                department
            )

            # 解析发布时间
            published = entry.get("published", "")
            if not published and hasattr(entry, "updated"):
                published = entry.updated

            article = {
                "title": entry.get("title", ""),
                "source": source_key,
                "source_name": feed.feed.get("title", source_key),
                "department": department,
                "content_type": content_type,
                "importance": importance,
                "url": entry.get("link", ""),
                "published": published,
                "crawled_at": datetime.now().isoformat(),
                **summary
            }
            articles.append(article)

    except Exception as e:
        print(f"  [ERROR] Failed to parse {source_key}: {e}")

    return articles


def crawl_etsy_shop(shop_name, url):
    """爬取 Etsy 竞品店铺"""
    articles = []
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # Etsy 店铺最新 listing标题和链接
        listings = soup.select("div[class*='listing'] a")
        for listing in listings[:10]:
            title = listing.get_text(strip=True)
            link = listing.get("href", "")
            if link and not link.startswith("http"):
                link = "https://www.etsy.com" + link

            if title and link:
                summary = generate_summary(title, "", "新玩法", "品牌")
                article = {
                    "title": title,
                    "source": f"etsy_{shop_name}",
                    "source_name": f"Etsy - {shop_name}",
                    "department": "品牌",
                    "content_type": "竞品动态",
                    "importance": "⭐",
                    "url": link,
                    "published": "",
                    "crawled_at": datetime.now().isoformat(),
                    **summary
                }
                articles.append(article)

        time.sleep(2)  # 避免请求过快

    except Exception as e:
        print(f"  [ERROR] Failed to crawl Etsy shop {shop_name}: {e}")

    return articles


def main():
    """主函数：抓取所有来源，生成 JSON"""
    print(f"[{datetime.now().isoformat()}] 开始抓取营销资讯...")

    all_articles = []

    # 1. 抓取 RSS 源
    print("抓取 RSS 源...")
    for source_key, url in RSS_SOURCES.items():
        print(f"  抓取 {source_key}...")
        articles = parse_rss_source(source_key, url)
        all_articles.extend(articles)
        time.sleep(1)

    # 2. 抓取竞品 Etsy 店铺
    print("抓取竞品网站...")
    for shop in COMPETITOR_SITES:
        print(f"  抓取 {shop['name']}...")
        articles = crawl_etsy_shop(shop["name"], shop["url"])
        all_articles.extend(articles)
        time.sleep(3)

    # 3. 按时间排序，最新的在前
    all_articles.sort(key=lambda x: x.get("crawled_at", ""), reverse=True)

    # 4. 写入 JSON 文件
    output_path = Path(__file__).parent.parent / "data" / "articles.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=2)

    print(f"完成！共抓取 {len(all_articles)}篇文章，保存到 {output_path}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: 本地测试爬虫**

Run: `python marketing-intelligence/scripts/crawl.py`
Expected: 脚本执行无报错，生成 `marketing-intelligence/data/articles.json`，包含抓取的资讯数据

- [ ] **Step 3: Commit**

```bash
git add marketing-intelligence/scripts/crawl.py
git commit -m "feat: add Python crawler script for marketing intelligence"
```

---

## Task 3: 编写 Hugo 配置文件

**Files:**
- Create: `marketing-intelligence/config.toml`

- [ ] **Step 1: 写 Hugo 配置**

```toml
baseURL = "https://callie-marketing.github.io/"
languageCode = "zh-CN"
title = "callie.com 营销资讯中心"
theme = []

[outputs]
home = ["HTML"]

[taxonomies]
department = "department"
content_type = "content_type"

[params]
description = "全球前沿营销玩法资讯，实时更新"
```

- [ ] **Step 2: Commit**

```bash
git add marketing-intelligence/config.toml
git commit -m "feat: add Hugo config.toml"
```

---

## Task 4: 编写 Hugo 列表页模板

**Files:**
- Create: `marketing-intelligence/layouts/index.html`

- [ ] **Step 1: 写 Hugo 模板**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ .Site.Title }}</title>
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <div class="container">
       <header class="header">
            <h1>🔥 {{ .Site.Title }}</h1>
            <p class="subtitle">全球前沿营销玩法资讯 · 每日更新</p>
        </header>

        <div class="search-bar">
            <input type="text" id="searchInput" placeholder="搜索资讯标题或摘要...">
            <button id="searchBtn">🔍</button>
        </div>

        <div class="tabs" id="deptTabs">
            <button class="tab active" data-dept="all">全部</button>
            <button class="tab" data-dept="社媒运营">社媒运营</button>
            <button class="tab" data-dept="红人营销">红人营销</button>
            <button class="tab" data-dept="广告投放">广告投放</button>
            <button class="tab" data-dept="用户运营">用户运营</button>
            <button class="tab" data-dept="SEO">SEO</button>
            <button class="tab" data-dept="品牌">品牌</button>
        </div>

        <div class="filters">
            <select id="typeFilter">
                <option value="all">全部类型</option>
                <option value="新玩法">新玩法</option>
                <option value="数据报告">数据报告</option>
                <option value="工具推荐">工具推荐</option>
                <option value="案例分享">案例分享</option>
                <option value="平台更新">平台更新</option>
                <option value="竞品动态">竞品动态</option>
            </select>
            <select id="importanceFilter">
                <option value="all">全部重要程度</option>
                <option value="⭐⭐⭐">⭐⭐⭐ 必读</option>
                <option value="⭐⭐">⭐⭐ 推荐</option>
                <option value="⭐">⭐ 了解</option>
            </select>
            <select id="timeFilter">
                <option value="all">全部时间</option>
                <option value="today">今天</option>
                <option value="week">本周</option>
                <option value="month">本月</option>
            </select>
        </div>

        <div id="articlesContainer" class="articles">
            <!-- 文章卡片由 JavaScript 动态渲染 -->
            <p class="loading">加载中...</p>
        </div>

        <footer class="footer">
            <p>由 GitHub Actions 自动更新 · 最后更新：<span id="lastUpdated">-</span></p>
        </footer>
    </div>

    <script src="/js/search.js"></script>
</body>
</html>
```

- [ ] **Step 2: Commit**

```bash
git add marketing-intelligence/layouts/index.html
git commit -m "feat: add Hugo index template"
```

---

## Task 5: 编写 CSS 样式

**Files:**
- Create: `marketing-intelligence/src/css/style.css`

- [ ] **Step 1: 写 CSS 样式**

```css
/* ===== 基础重置 ===== */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    background-color: #f5f5f5;
    color: #333;
    line-height: 1.6;
}

/* ===== 容器 ===== */
.container {
    max-width: 960px;
    margin: 0 auto;
    padding: 20px;
}

/* ===== 头部 ===== */
.header {
    text-align: center;
    padding: 30px 020px;
    border-bottom: 2px solid #e0e0e0;
    margin-bottom: 24px;
}

.header h1 {
    font-size: 28px;
    color: #d32f2f;
    margin-bottom: 8px;
}

.subtitle {
    color: #888;
    font-size: 14px;
}

/* ===== 搜索栏 ===== */
.search-bar {
    display: flex;
    gap: 8px;
    margin-bottom: 20px;
}

.search-bar input {
    flex: 1;
    padding: 12px 16px;
    font-size: 16px;
    border: 2px solid #ddd;
    border-radius: 8px;
    outline: none;
    transition: border-color 0.2s;
}

.search-bar input:focus {
    border-color: #d32f2f;
}

.search-bar button {
    padding: 12px 20px;
    font-size: 16px;
    background: #d32f2f;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
}

/* ===== Tab 切换 ===== */
.tabs {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 16px;
}

.tab {
    padding: 8px 16px;
    border: 2px solid #ddd;
    border-radius: 20px;
    background: white;
    cursor: pointer;
    font-size: 14px;
    transition: all 0.2s;
}

.tab:hover {
    border-color: #d32f2f;
    color: #d32f2f;
}

.tab.active {
    background: #d32f2f;
    color: white;
    border-color: #d32f2f;
}

/* ===== 筛选器 ===== */
.filters {
    display: flex;
    gap: 12px;
    margin-bottom: 24px;
    flex-wrap: wrap;
}

.filters select {
    padding: 8px 12px;
    border: 2px solid #ddd;
    border-radius: 8px;
    background: white;
    cursor: pointer;
    font-size: 14px;
    outline: none;
}

/* ===== 文章卡片 ===== */
.articles {
    display: grid;
    gap: 16px;
}

.article-card {
    background: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    transition: transform 0.2s, box-shadow 0.2s;
}

.article-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0,0,0,0.12);
}

.article-header {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    margin-bottom: 12px;
}

.article-importance {
    font-size: 14px;
    white-space: nowrap;
}

.article-title {
    flex: 1;
    font-size: 18px;
    font-weight: 600;
    color: #1a1a1a;
}

.article-title a {
    color: inherit;
    text-decoration: none;
}

.article-title a:hover {
    color: #d32f2f;
    text-decoration: underline;
}

.article-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 12px;
    font-size: 13px;
    color: #888;
}

.article-meta .tag {
    padding: 2px 8px;
    border-radius: 4px;
    background: #f0f0f0;
}

.article-meta .dept {
    background: #fff3e0;
    color: #e65100;
}

.article-summary {
    margin-bottom: 12px;
    font-size: 14px;
    color: #555;
}

.article-summary p {
    margin-bottom: 6px;
}

.article-summary strong {
    color: #333;
}

.article-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.article-link {
    display: inline-block;
    padding: 8px 16px;
    background: #d32f2f;
    color: white;
    border-radius: 6px;
    text-decoration: none;
    font-size: 14px;
}

.article-link:hover {
    background: #b71c1c;
}

.article-date {
    font-size: 12px;
    color: #aaa;
}

/* ===== 加载状态 ===== */
.loading {
    text-align: center;
    padding: 40px;
    color: #888;
}

/* ===== 底部 ===== */
.footer {
    text-align: center;
    padding: 30px 0;
    margin-top: 40px;
    border-top: 1px solid #e0e0e0;
    color: #aaa;
    font-size: 13px;
}

/* ===== 响应式 ===== */
@media (max-width: 600px) {
    .container {
        padding: 12px;
    }

    .header h1 {
        font-size: 22px;
    }

    .filters {
        flex-direction: column;
    }

    .article-header {
        flex-direction: column;
    }
}
```

- [ ] **Step 2: Commit**

```bash
git add marketing-intelligence/src/css/style.css
git commit -m "feat: add CSS styles for marketing intelligence hub"
```

---

## Task 6: 编写 JavaScript 搜索筛选逻辑

**Files:**
- Create: `marketing-intelligence/src/js/search.js`

- [ ] **Step 1: 写 JavaScript 搜索筛选逻辑**

```javascript
/**
 * 营销资讯中心 - 搜索和筛选逻辑
 * 加载 data/articles.json，在浏览器端进行搜索和筛选
 */

let allArticles = [];
let currentFilters = {
    department: "all",
    contentType: "all",
    importance: "all",
    timeRange: "all",
    keyword: ""
};

// ========== 数据加载 ==========

async function loadArticles() {
    try {
        const resp = await fetch("/data/articles.json");
        if (!resp.ok) throw new Error("Failed to load articles");
        allArticles = await resp.json();
        renderArticles();
        updateLastUpdated();
    } catch (err) {
        document.getElementById("articlesContainer").innerHTML =
            '<p class="loading">加载失败，请刷新重试</p>';
        console.error(err);
    }
}

function updateLastUpdated() {
    if (allArticles.length === 0) return;
    const latest = allArticles[0].crawled_at;
    const date = new Date(latest);
    document.getElementById("lastUpdated").textContent =
        date.toLocaleString("zh-CN");
}

// ========== 筛选逻辑 ==========

function filterArticles() {
    const today = new Date();
    const startOfToday = new Date(today.getFullYear(), today.getMonth(), today.getDate());
    const startOfWeek = new Date(startOfToday);
    startOfWeek.setDate(startOfWeek.getDate() - startOfWeek.getDay());
    const startOfMonth = new Date(today.getFullYear(), today.getMonth(), 1);

    return allArticles.filter(article => {
        // 部门筛选
        if (currentFilters.department !== "all" &&
            article.department !== currentFilters.department) {
            return false;
        }

        // 类型筛选
        if (currentFilters.contentType !== "all" &&
            article.content_type !== currentFilters.contentType) {
            return false;
        }

        // 重要程度筛选
        if (currentFilters.importance !== "all" &&
            article.importance !== currentFilters.importance) {
            return false;
        }

        // 时间范围筛选
        if (currentFilters.timeRange !== "all") {
            const published = parseDate(article.published);
            if (!published) {
                if (currentFilters.timeRange !== "all") return false;
            } else if (currentFilters.timeRange === "today" && published < startOfToday) {
                return false;
            } else if (currentFilters.timeRange === "week" && published < startOfWeek) {
                return false;
            } else if (currentFilters.timeRange === "month" && published < startOfMonth) {
                return false;
            }
        }

        // 关键词搜索（标题 + 摘要）
        if (currentFilters.keyword) {
            const kw = currentFilters.keyword.toLowerCase();
            const searchable = (
                article.title + " " +
                (article["一句话结论"] || "") + " " +
                (article["为什么重要"] || "") + " " +
                (article["可以怎么用"] || "")
            ).toLowerCase();
            if (!searchable.includes(kw)) return false;
        }

        return true;
    });
}

function parseDate(dateStr) {
    if (!dateStr) return null;
    try {
        return new Date(dateStr);
    } catch {
        return null;
    }
}

// ========== 渲染逻辑 ==========

function renderArticles() {
    const container = document.getElementById("articlesContainer");
    const filtered = filterArticles();

    if (filtered.length === 0) {
        container.innerHTML = '<p class="loading">暂无符合条件的资讯</p>';
        return;
    }

    container.innerHTML = filtered.map(article => {
        const date = parseDate(article.published);
        const dateStr = date ? date.toLocaleDateString("zh-CN") : "未知时间";

        return `
        <div class="article-card">
            <div class="article-header">
                <span class="article-importance">${article.importance}</span>
                <h3 class="article-title">
                    <a href="${article.url}" target="_blank" rel="noopener">${article.title}</a>
                </h3>
            </div>
            <div class="article-meta">
                <span class="tag dept">${article.department}</span>
                <span class="tag">${article.content_type}</span>
                <span class="tag">来源：${article.source_name}</span>
                <span class="tag">${dateStr}</span>
            </div>
            <div class="article-summary">
                <p><strong>📌 一句话结论：</strong>${article["一句话结论"] || "-"}</p>
                <p><strong>💡 为什么重要：</strong>${article["为什么重要"] || "-"}</p>
                <p><strong>🎯 可以怎么用：</strong>${article["可以怎么用"] || "-"}</p>
            </div>
            <div class="article-footer">
                <a class="article-link" href="${article.url}" target="_blank" rel="noopener">查看原文 →</a>
            </div>
        </div>
        `;
    }).join("");
}

// ========== 事件绑定 ==========

function initEventListeners() {
    // Tab 切换
    document.querySelectorAll(".tab").forEach(tab => {
        tab.addEventListener("click", () => {
            document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
            tab.classList.add("active");
            currentFilters.department = tab.dataset.dept;
            renderArticles();
        });
    });

    //筛选下拉框
    document.getElementById("typeFilter").addEventListener("change", e => {
        currentFilters.contentType = e.target.value;
        renderArticles();
    });

    document.getElementById("importanceFilter").addEventListener("change", e => {
        currentFilters.importance = e.target.value;
        renderArticles();
    });

    document.getElementById("timeFilter").addEventListener("change", e => {
        currentFilters.timeRange = e.target.value;
        renderArticles();
    });

    // 搜索框（实时搜索）
    const searchInput = document.getElementById("searchInput");
    let searchTimeout;
    searchInput.addEventListener("input", () => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            currentFilters.keyword = searchInput.value.trim();
            renderArticles();
        }, 300);
    });

    document.getElementById("searchBtn").addEventListener("click", () => {
        currentFilters.keyword = searchInput.value.trim();
        renderArticles();
    });
}

// ========== 初始化 ==========

document.addEventListener("DOMContentLoaded", () => {
    initEventListeners();
    loadArticles();
});
```

- [ ] **Step 2: Commit**

```bash
git add marketing-intelligence/src/js/search.js
git commit -m "feat: add browser-side search and filter logic"
```

---

## Task 7: 编写 GitHub Actions 工作流

**Files:**
- Create: `marketing-intelligence/.github/workflows/daily-crawl-deploy.yml`

- [ ] **Step 1: 写 GitHub Actions 工作流**

```yaml
name: Daily Crawl and Deploy

on:
  schedule:
    - cron: '0 1 * * *'  # 每天凌晨 1 点 UTC = 北京时间 9 点
  workflow_dispatch:       # 手动触发

jobs:
  crawl-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install Python dependencies
        run: |
          pip install feedparser requests beautifulsoup4

      - name: Run crawler
        run: python scripts/crawl.py

      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v3
        with:
          hugo-version: '0.131.0'

      - name: Build Hugo site
        run: hugo --destination public

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./public
```

- [ ] **Step 2: Commit**

```bash
git add marketing-intelligence/.github/workflows/daily-crawl-deploy.yml
git commit -m "feat: add GitHub Actions daily crawl and deploy workflow"
```

---

## Task 8: 编写 README

**Files:**
- Create: `marketing-intelligence/README.md`

- [ ] **Step 1: 写 README**

```markdown
# callie.com 营销资讯中心

一个轻量静态网页，自动化抓取全球营销媒体、社交媒体平台和竞品网站的最新资讯，支持搜索和筛选，通过钉钉链接分享给团队访问。

## 功能特性

- ✅ 全自动抓取（RSS + 竞品网站）
- ✅ 每日凌晨自动更新
- ✅ 浏览器端搜索 + 多维度筛选
- ✅ 钉钉分享链接访问，无需登录

## 技术栈

- Python 爬虫（feedparser + requests + beautifulsoup4）
- Hugo静态网站生成
- GitHub Pages 免费托管
- GitHub Actions 自动化部署

## 本地开发

### 前置要求

- Python 3.11+
- Hugo Extended0.131+

### 安装依赖

```bash
pip install feedparser requests beautifulsoup4
```

### 本地运行爬虫

```bash
python scripts/crawl.py
```

### 本地预览网站

```bash
hugo server -D
```

访问 http://localhost:1313 查看。

## 部署说明

本项目使用 GitHub Actions 每天凌晨自动运行爬虫并部署到 GitHub Pages。

1. 将 `marketing-intelligence` 目录推送到 GitHub 仓库
2. 在仓库 Settings → Pages 中启用 GitHub Pages，选择 `gh-pages` 分支
3. 在仓库 Settings → Actions 中添加 `GITHUB_TOKEN` 权限
4. 启用 Actions 工作流（默认已配置每日运行）

## 内容来源

### 一级来源（每周必读）

- Adweek
- Marketing Week
- Social Media Today
- Search Engine Journal

### 二级来源（平台官方）

- TikTok for Business Blog
- YouTube Blog
- Google Ads Blog
- Meta for Business

### 竞品动态

- wanderprints (Etsy)
- macorner (Etsy)
- pawsionate (Etsy)

## 目录结构

```
marketing-intelligence/
├── config.toml              # Hugo 配置
├── data/
│   └── articles.json       #爬虫生成的数据（gitignore）
├── scripts/
│   └── crawl.py            # Python 爬虫脚本
├── layouts/
│   └── index.html         # Hugo 模板
└── src/
    ├── css/style.css       # 样式
    └── js/search.js       # 搜索筛选逻辑
```
```

- [ ] **Step 2: Commit**

```bash
git add marketing-intelligence/README.md
git commit -m "docs: add README for marketing intelligence hub"
```

---

## Task 9: 本地端到端测试

- [ ] **Step 1: 安装依赖并运行爬虫**

```bash
pip install feedparser requests beautifulsoup4
python marketing-intelligence/scripts/crawl.py
```

Expected: 成功生成 `marketing-intelligence/data/articles.json`，无报错

- [ ] **Step 2: 本地构建 Hugo 站点**

```bash
cd marketing-intelligence
hugo --destination public
```

Expected: 成功生成 `public/` 目录，包含 `index.html`、`css/style.css`、`js/search.js`

- [ ] **Step 3: 本地预览**

```bash
hugo server -D
```

Expected: 浏览器访问 http://localhost:1313 能看到资讯页面，搜索和筛选功能正常

- [ ] **Step 4: Commit 所有文件**

```bash
git add .
git commit -m "feat: complete marketing intelligence hub v1"
```

---

## Spec 自查

1. ✅ 内容抓取 — Task 2 爬虫脚本覆盖所有 RSS 源和竞品网站
2. ✅ 搜索功能 — Task 6 JavaScript 实现浏览器端全文搜索
3. ✅ 筛选功能 — Task 6 实现部门/类型/重要程度/时间范围筛选
4. ✅ 页面展示 — Task 4 Hugo 模板 + Task 5 CSS + Task 6 JS
5. ✅ 自动化部署 — Task 7 GitHub Actions 工作流
6. ✅ 每天更新 — Task 7 Cron 配置每天凌晨执行
7. ✅钉钉分享访问 — 部署到 GitHub Pages 后分享链接即可

---

Plan complete and saved to `docs/superpowers/plans/2026-06-09-marketing-intelligence-hub-plan.md`.

**Two execution options:**

**1. Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** — Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?