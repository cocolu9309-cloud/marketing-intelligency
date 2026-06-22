# scripts/crawl_products.py
"""
Callie.com 产品爬虫
首次使用：python scripts/crawl_products.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import httpx, json, re, time
from bs4 import BeautifulSoup

from db import get_db, get_db_path, DB_PATH

CALLIE_BASE = "https://www.callie.com"

# 导航栏分类（需手动确认，实际应从页面抓取）
NAV_CATEGORIES = {
    "personalized-gifts": "个性化礼品",
    "pet-memory": "宠物纪念品",
    "home-decor": "家居装饰",
}

def init_db():
    db_path = get_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_en TEXT NOT NULL,
            name_cn TEXT,
            category TEXT,
            tags TEXT,
            image_url TEXT,
            description TEXT,
            occasions TEXT,
            status TEXT DEFAULT '在售',
            crawled_at TEXT
        )
    """)
    c.execute("CREATE INDEX IF NOT EXISTS idx_category ON products(category)")
    conn.commit()
    conn.close()

def crawl_category(category_slug: str, category_cn: str) -> list:
    """爬取单个分类下的所有产品"""
    url = f"{CALLIE_BASE}/{category_slug}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    products = []
    try:
        resp = httpx.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(resp.text, "html.parser")
        # 注意：实际选择器需要根据 Callie.com 实际页面结构调整
        items = soup.select(".product-item a[href*='/product/']")
        for item in items:
            href = item.get("href", "")
            name_en = item.select_one(".product-name").get_text(strip=True) if item.select_one(".product-name") else ""
            img = item.select_one("img[src]")["src"] if item.select_one("img[src]") else ""
            if href and name_en:
                products.append({
                    "name_en": name_en,
                    "category": category_cn,
                    "image_url": img if img.startswith("http") else CALLIE_BASE + img,
                    "href": href if href.startswith("http") else CALLIE_BASE + href,
                })
        print(f"  [{category_cn}] 找到 {len(items)} 个产品")
    except Exception as e:
        print(f"  [{category_cn}] 爬取失败: {e}")
    return products

def crawl_product_detail(product: dict) -> dict:
    """爬取单个产品详情页"""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        resp = httpx.get(product["href"], headers=headers, timeout=30)
        soup = BeautifulSoup(resp.text, "html.parser")
        # 实际选择器需根据页面调整
        desc_elem = soup.select_one(".product-description")
        product["description"] = desc_elem.get_text(strip=True) if desc_elem else ""
        # 适用场景从描述中提取关键词判断
        occasions = []
        desc_lower = product["description"].lower()
        if any(w in desc_lower for w in ["birthday", "生日"]): occasions.append("生日")
        if any(w in desc_lower for w in ["wedding", "婚礼"]): occasions.append("婚礼")
        if any(w in desc_lower for w in ["anniversary", "纪念日"]): occasions.append("纪念日")
        if any(w in desc_lower for w in ["mother", "母亲"]): occasions.append("母亲节")
        if any(w in desc_lower for w in ["father", "父亲"]): occasions.append("父亲节")
        if any(w in desc_lower for w in ["pet", "宠物"]): occasions.append("宠物")
        product["occasions"] = json.dumps(occasions, ensure_ascii=False)
        product["tags"] = json.dumps([product["category"]], ensure_ascii=False)
        time.sleep(0.5)  # 避免请求过快
    except Exception as e:
        print(f"  详情页失败: {e}")
    return product

def save_products(products: list):
    conn = get_db()
    c = conn.cursor()
    # 清空旧数据
    c.execute("DELETE FROM products")
    for p in products:
        c.execute("""
            INSERT INTO products (name_en, name_cn, category, tags, image_url, description, occasions, status, crawled_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, '在售', datetime('now'))
        """, (p.get("name_en"), p.get("name_cn"), p.get("category"), p.get("tags"),
              p.get("image_url"), p.get("description"), p.get("occasions")))
    conn.commit()
    conn.close()
    print(f"\n已保存 {len(products)} 个产品到数据库")

def main():
    print("开始爬取 Callie.com 产品...")
    all_products = []
    for slug, cn in NAV_CATEGORIES.items():
        print(f"爬取分类: {cn}")
        prods = crawl_category(slug, cn)
        for p in prods:
            detail = crawl_product_detail(p)
            all_products.append(detail)
    save_products(all_products)
    print("完成!")

if __name__ == "__main__":
    init_db()
    main()