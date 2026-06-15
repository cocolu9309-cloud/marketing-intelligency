"""
Marketing Intelligence Crawler
爬取 RSS 订阅源和 Etsy 竞品店铺数据
"""

import json
import os
import requests
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup
import feedparser

# 获取脚本所在目录的父目录（即项目根目录）
REPO_ROOT = Path(__file__).parent.parent

# RSS 订阅源配置
RSS_SOURCES = {
    "adweek": "https://www.adweek.com/feed/",
    "marketing_week": "https://www.marketingweek.com/feed/",
    "social_media_today": "https://www.socialmediatoday.com/rss.xml",
    "search_engine_journal": "https://www.searchenginejournal.com/feed/",
    "tiktok_business": "https://business.tiktok.com/blog/rss",
    "youtube_blog": "https://blog.youtube/rss.xml",
    "google_ads_blog": "https://adsdeveloper.blogspot.com/feeds/posts/default",
    "meta_business": "https://www.facebook.com/business/news/rss",
    # 用户洞察
    "omnisend": "https://www.omnisend.com/blog/feed/",
    "hootsuite": "https://blog.hootsuite.com/feed/",
    "brandwatch": "https://www.brandwatch.com/feed/",
    # 定制礼品行业趋势
    "practical_ecommerce": "https://www.practicalecommerce.com/feed/",
    "small_business_trends": "https://smallbiztrends.com/feed/",
    "printful": "https://www.printful.com/blog/feed",
    # 新增：研究数据来源
    "social_media_examiner": "https://www.socialmediaexaminer.com/feed/",
    "adverity": "https://blog.adverity.com/feed/",
    # Google News 竞品监控 RSS
    "google_news_etsy": "https://news.google.com/news/rss/search?q=etsy+custom+gift&hl=en-US&gl=US&ceid=US:en",
    "google_news_print_on_demand": "https://news.google.com/news/rss/search?q=print+on+demand+custom+gift&hl=en-US&gl=US&ceid=US:en",
    "google_news_personalized_gift": "https://news.google.com/news/rss/search?q=personalized+gift+trend&hl=en-US&gl=US&ceid=US:en",
}

# Etsy 竞品店铺配置
ETSY_SHOPS = [
    "wanderprints",
    "macorner",
    "pawsionate",
]

# 部门归属映射
DEPARTMENT_MAPPING = {
    # 品牌
    "adweek": "品牌",
    "marketing_week": "品牌",
    # SEO
    "search_engine_journal": "SEO",
    # 广告投放
    "google_ads_blog": "广告投放",
    "meta_business": "广告投放",
    # 用户洞察
    "omnisend": "用户洞察",
    "hootsuite": "用户洞察",
    "brandwatch": "用户洞察",
    # 竞品最新动态
    "printful": "竞品最新动态",
    # 社交媒体运营
    "social_media_today": "社交媒体运营",
    "tiktok_business": "社交媒体运营",
    "youtube_blog": "社交媒体运营",
    # 社媒热门内容（临时用 practical_ecommerce）
    "practical_ecommerce": "社媒热门内容",
    # 定制礼品最新行业趋势
    "small_business_trends": "定制礼品最新行业趋势",
    # 新增：研究数据来源
    "social_media_examiner": "社媒热门内容",
    "adverity": "数据",
    # Google News 竞品监控
    "google_news_etsy": "竞品最新动态",
    "google_news_print_on_demand": "竞品最新动态",
    "google_news_personalized_gift": "定制礼品最新行业趋势",
}

# 内容类型关键词
CONTENT_TYPE_KEYWORDS = {
    "趋势": ["趋势", "趋势报告", "预测", "展望", "未来", "forecast", "trend"],
    "案例": ["案例", "案例分析", "成功案例", "案例研究", "case study", "example"],
    "教程": ["教程", "指南", "如何", "技巧", "步骤", "入门", "tutorial", "guide", "how to", "tips"],
    "工具": ["工具", "工具推荐", "软件", "平台", "tool", "software", "platform"],
    "数据": ["数据", "报告", "分析", "研究", "调研", "data", "report", "research", "analysis"],
    "观点": ["观点", "看法", "评论", "思考", "opinion", "commentary", "perspective"],
}

# 重要程度关键词
IMPORTANCE_KEYWORDS = {
    "高": ["重大", "重要", "首发", "独家", "必读", "breaking", "major", "important", "exclusive"],
    "中": ["推荐", "值得看", "参考", "interesting", "worth reading"],
    "低": ["一般", "可选", "optional", "general"],
}


def determine_content_type(title: str, description: str = "") -> str:
    """根据标题和描述判断内容类型"""
    text = (title + " " + (description or "")).lower()

    for content_type, keywords in CONTENT_TYPE_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in text:
                return content_type
    return "其他"


def determine_importance(title: str, description: str = "") -> str:
    """根据标题和描述判断重要程度"""
    text = (title + " " + (description or "")).lower()

    for importance, keywords in IMPORTANCE_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in text:
                return importance
    return "中"


def generate_summary(title: str, content_type: str, department: str, source_name: str) -> dict:
    """根据内容类型和部门生成摘要信息"""
    # 一句话结论：取标题前30字
    one_sentence = title[:30] + "..." if len(title) > 30 else title

    # 为什么重要：根据内容类型生成
    why_important_map = {
        "趋势": f"{source_name}发布的行业趋势分析，帮助把握市场方向",
        "案例": f"{source_name}精选成功案例，可借鉴的营销实践",
        "教程": f"{source_name}提供的实操教程，适合学习参考",
        "工具": f"{source_name}推荐的高效工具，提升工作效率",
        "数据": f"{source_name}发布的数据报告，提供决策依据",
        "观点": f"{source_name}专家观点，引发思考",
        "其他": f"来自{source_name}的营销资讯",
    }
    why_important = why_important_map.get(content_type, why_important_map["其他"])

    # 可以怎么用：根据部门生成
    how_to_use_map = {
        "SEO": "可用于SEO策略优化、关键词研究、技术参考",
        "品牌": "可用于品牌建设、创意灵感、市场定位参考",
        "广告投放": "可用于广告投放优化、预算分配、创意参考",
        "用户洞察": "可用于用户行为分析、CRM优化、会员运营参考",
        "竞品最新动态": "可用于竞品监控、市场分析、差异化策略参考",
        "社交媒体运营": "可用于社交媒体内容策划、平台运营策略借鉴",
        "社媒热门内容": "可用于内容选题、热点追踪、病毒传播规律参考",
        "定制礼品最新行业趋势": "可用于选品决策、行业洞察、定制礼品趋势参考",
        "数据": "可用于数据驱动决策、营销效果评估、趋势分析参考",
    }
    how_to_use = how_to_use_map.get(department, "可用于营销策划参考")

    return {
        "one_sentence": one_sentence,
        "why_important": why_important,
        "how_to_use": how_to_use,
    }


def parse_rss_source(source_key: str, source_url: str) -> list:
    """解析 RSS 订阅源"""
    articles = []

    try:
        feed = feedparser.parse(source_url)

        for entry in feed.entries:
            # 获取发布时间
            published = None
            if hasattr(entry, 'published'):
                try:
                    published = datetime(*entry.published_parsed[:6]).isoformat()
                except Exception:
                    published = datetime.now().isoformat()
            elif hasattr(entry, 'updated'):
                try:
                    published = datetime(*entry.updated_parsed[:6]).isoformat()
                except Exception:
                    published = datetime.now().isoformat()
            else:
                published = datetime.now().isoformat()

            # 获取URL
            url = entry.get('link', '')

            # 获取标题
            title = entry.get('title', '无标题')

            # 获取描述
            description = ''
            if hasattr(entry, 'summary'):
                description = entry.summary
            elif hasattr(entry, 'description'):
                description = entry.description

            # 清理HTML标签
            if description:
                soup = BeautifulSoup(description, 'html.parser')
                description = soup.get_text()

            # 确定内容类型和重要程度
            content_type = determine_content_type(title, description)
            importance = determine_importance(title, description)

            # 获取部门
            department = DEPARTMENT_MAPPING.get(source_key, "其他")

            # 生成来源名称
            source_name_map = {
                "adweek": "Adweek",
                "marketing_week": "Marketing Week",
                "social_media_today": "Social Media Today",
                "search_engine_journal": "Search Engine Journal",
                "tiktok_business": "TikTok Business",
                "youtube_blog": "YouTube Blog",
                "google_ads_blog": "Google Ads Developer Blog",
                "meta_business": "Meta Business",
                "omnisend": "Omnisend",
                "hootsuite": "Hootsuite",
                "brandwatch": "Brandwatch",
                "practical_ecommerce": "Practical Ecommerce",
                "small_business_trends": "Small Business Trends",
                "printful": "Printful",
                "social_media_examiner": "Social Media Examiner",
                "adverity": "Adverity",
                "google_news_etsy": "Google News (Etsy)",
                "google_news_print_on_demand": "Google News (Print on Demand)",
                "google_news_personalized_gift": "Google News (Personalized Gift)",
            }
            source_name = source_name_map.get(source_key, source_key)

            # 生成摘要
            summary = generate_summary(title, content_type, department, source_name)

            article = {
                "title": title,
                "source": source_key,
                "source_name": source_name,
                "department": department,
                "content_type": content_type,
                "importance": importance,
                "url": url,
                "published": published,
                "crawled_at": datetime.now().isoformat(),
                "one_sentence": summary["one_sentence"],
                "why_important": summary["why_important"],
                "how_to_use": summary["how_to_use"],
            }
            articles.append(article)

    except Exception as e:
        print(f"Error parsing RSS {source_key}: {e}")

    return articles


def crawl_etsy_shop(shop_name: str) -> list:
    """爬取 Etsy 店铺信息"""
    articles = []

    try:
        url = f"https://www.etsy.com/shop/{shop_name}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # 尝试获取店铺名称
        shop_title = soup.find('h1', class_='shop-name')
        if shop_title:
            shop_title = shop_title.get_text().strip()
        else:
            shop_title = shop_name

        # 获取商品列表（示例：获取前几个商品标题）
        listings = soup.find_all('div', class_='listing-link')

        for idx, listing in enumerate(listings[:10]):  # 限制最多10个
            title_elem = listing.find('a', class_='listing-title')
            if title_elem:
                title = title_elem.get_text().strip()
            else:
                title = f"{shop_title} 商品 {idx + 1}"

            link_elem = listing.find('a', href=True)
            item_url = link_elem['href'] if link_elem else url

            # Etsy 店铺属于"竞品分析"类型
            content_type = "案例"  # 竞品案例

            # 生成摘要
            summary = generate_summary(title, content_type, "竞品分析", shop_title)

            article = {
                "title": title,
                "source": f"etsy_{shop_name}",
                "source_name": f"Etsy-{shop_title}",
                "department": "竞品分析",
                "content_type": content_type,
                "importance": "中",
                "url": item_url,
                "published": datetime.now().isoformat(),
                "crawled_at": datetime.now().isoformat(),
                "one_sentence": summary["one_sentence"],
                "why_important": f"竞品{shop_title}的商品分析",
                "how_to_use": "用于竞品调研、市场分析、选品参考",
            }
            articles.append(article)

    except Exception as e:
        print(f"Error crawling Etsy shop {shop_name}: {e}")

    return articles


def main():
    """主函数"""
    all_articles = []

    # 爬取 RSS 订阅源
    print("Crawling RSS sources...")
    for source_key, source_url in RSS_SOURCES.items():
        print(f"  Fetching {source_key}...")
        articles = parse_rss_source(source_key, source_url)
        all_articles.extend(articles)
        print(f"    Found {len(articles)} articles")

    # 爬取 Etsy 竞品店铺
    print("Crawling Etsy shops...")
    for shop_name in ETSY_SHOPS:
        print(f"  Fetching {shop_name}...")
        articles = crawl_etsy_shop(shop_name)
        all_articles.extend(articles)
        print(f"    Found {len(articles)} articles")

    # 按发布时间排序（最新的在前）
    all_articles.sort(key=lambda x: x.get('published', ''), reverse=True)

    # 写入 JSON 文件（GitHub Pages 从 marketing-intelligency/data/ 读取）
    output_path = REPO_ROOT / "data" / "articles.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=2)

    print(f"\nTotal articles: {len(all_articles)}")
    print(f"Output written to: {output_path}")


if __name__ == "__main__":
    main()