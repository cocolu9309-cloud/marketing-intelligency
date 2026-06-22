# scripts/product_db.py
"""产品库查询和匹配模块"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import json
from typing import List, Dict

from db import get_db, DB_PATH

def search_products(keywords: List[str], top_n: int = 3) -> List[Dict]:
    """根据关键词搜索产品，返回 Top N"""
    conn = get_db()
    c = conn.cursor()
    # Search each keyword separately, OR all conditions
    conditions = []
    params = []
    for kw in keywords:
        pattern = f"%{kw}%"
        conditions.append("(name_en LIKE ? OR description LIKE ? OR tags LIKE ? OR occasions LIKE ?)")
        params.extend([pattern, pattern, pattern, pattern])
    where_clause = " OR ".join(conditions) if conditions else "1=1"
    sql = f"""
        SELECT id, name_en, name_cn, category, tags, image_url, description, occasions
        FROM products
        WHERE {where_clause}
        LIMIT ?
    """
    params.append(top_n)
    c.execute(sql, params)
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_all_products() -> List[Dict]:
    """获取所有产品"""
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

if __name__ == "__main__":
    # 测试
    results = search_products(["pet", "memory"], 3)
    print(f"Found {len(results)} products")
    for p in results:
        print(f"  - {p['name_en']} ({p['category']})")