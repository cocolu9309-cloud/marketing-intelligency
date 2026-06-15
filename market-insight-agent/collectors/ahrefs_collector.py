import httpx
import json
from datetime import datetime
from knowledge_base.db import SessionLocal, CompetitorActionDB, CompetitorDB
from config import settings
import uuid

AHREFS_MCP_KEY = "wq8X.MbAOsd7LEWgStWIpQOSh6TpPcjM3MjdpVXFvVldid2szekJVYjVveUViV29kam00Qnc3K2FwTW5oS1dJKzMyemZ6bThPa0I2b0x6NFJ1K1pGd21yZlNPRkNraE1xU2RpZ3FpNFA0MzVreWUyd2dhakZNdk41Y2w1RU5YNUVmbmZxRlRleGtPaEJHRXM.qBpr"

async def call_ahrefs_mcp(method: str, params: dict) -> dict:
    """调用Ahrefs MCP"""
    url = "https://api.ahrefs.com/mcp/mcp"
    headers = {
        "Authorization": f"Bearer {AHREFS_MCP_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": str(uuid.uuid4())[:8]
    })

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(url, content=payload, headers=headers)
        response.raise_for_status()
        return response.json()

def parse_competitors_from_response(result: dict) -> list:
    """从MCP响应中提取竞品列表"""
    try:
        content = result.get("result", {}).get("content", [])
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                text = item.get("text", "")
                if "competitors" in text:
                    # 找到JSON开始位置
                    json_start = text.find("{")
                    json_end = text.rfind("}") + 1
                    if json_start >= 0 and json_end > json_start:
                        json_str = text[json_start:json_end]
                        data = json.loads(json_str)
                        return data.get("competitors", [])
    except Exception as e:
        print(f"解析竞品数据失败: {e}")
    return []

async def collect_competitor_seo_data(domain: str) -> int:
    """采集竞品SEO数据"""
    try:
        result = await call_ahrefs_mcp("tools/call", {
            "name": "site-explorer-organic-competitors",
            "arguments": {
                "target": domain,
                "select": "competitor_domain,traffic,keywords_competitor",
                "country": "US",
                "date": "2024-01-01",
                "limit": 5,
                "mode": "subdomains"
            }
        })

        competitors = parse_competitors_from_response(result)
        if not competitors:
            return 0

        db = SessionLocal()
        try:
            added = 0
            for comp in competitors:
                competitor_domain = comp.get("competitor_domain", "")

                # 检查是否已存在
                existing = db.query(CompetitorActionDB).filter(
                    CompetitorActionDB.competitor == domain,
                    CompetitorActionDB.description.contains(competitor_domain)
                ).first()

                if existing:
                    continue

                traffic = comp.get("traffic", 0)
                action = CompetitorActionDB(
                    id=f"CA-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6]}",
                    competitor=domain,
                    action_type="SEO竞品",
                    description=f"有机搜索竞品: {competitor_domain} (流量: {traffic:,})",
                    possible_goal="SEO流量竞争",
                    target_audience=None,
                    evidence_url=None,
                    should_follow=False,
                    suggested_action=f"分析{competitor_domain}的关键词策略",
                    created_at=datetime.now()
                )
                db.add(action)
                added += 1

            db.commit()
            return added
        finally:
            db.close()
    except Exception as e:
        print(f"采集{domain}竞品数据失败: {e}")
        return 0

async def collect_all_competitors():
    """为所有竞品采集SEO数据"""
    db = SessionLocal()
    try:
        competitors = db.query(CompetitorDB).limit(20).all()  # 限制每次采集20个
        total = 0
        for comp in competitors:
            url = comp.url or ""
            if url:
                domain = url.replace("https://", "").replace("http://", "").split("/")[0]
                if domain:
                    count = await collect_competitor_seo_data(domain)
                    if count > 0:
                        print(f"{domain}: +{count}条")
                        total += count
        print(f"总共获取{total}条竞品动态")
    finally:
        db.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(collect_all_competitors())