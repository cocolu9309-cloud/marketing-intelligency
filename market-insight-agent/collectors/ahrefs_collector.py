import httpx
import json
from datetime import datetime
from knowledge_base.db import SessionLocal, SearchOpportunityDB, CompetitorActionDB
from config import settings
import uuid

async def call_ahrefs_mcp(method: str, params: dict) -> dict:
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            settings.AHREFS_MCP_URL,
            json={"method": method, "params": params},
        )
        response.raise_for_status()
        return response.json()

async def collect_keyword_data():
    """采集关键词数据"""
    try:
        result = await call_ahrefs_mcp("ahrefs.keywords", {
            "keywords": settings.GIFT_KEYWORDS,
            "limit": 100,
        })
        db = SessionLocal()
        try:
            for item in result.get("keywords", []):
                search_opp = SearchOpportunityDB(
                    id=f"SO-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6]}",
                    keyword=item.get("keyword", ""),
                    search_intent=classify_intent(item.get("keyword", "")),
                    recommended_page_type="产品页",
                    priority=calculate_priority(item),
                    search_volume=item.get("search_volume"),
                    competition=item.get("competition"),
                    created_at=datetime.now(),
                )
                db.add(search_opp)
            db.commit()
        finally:
            db.close()
    except Exception as e:
        print(f"关键词采集失败: {e}")

def classify_intent(keyword: str) -> str:
    """分类搜索意图"""
    purchase_words = ["buy", "shop", "order", "定制", "个性化"]
    info_words = ["how to", "what is", "教程", "是什么"]
    for word in purchase_words:
        if word in keyword.lower():
            return "购买型"
    for word in info_words:
        if word in keyword.lower():
            return "信息型"
    return "灵感型"

def calculate_priority(item: dict) -> int:
    """计算优先级"""
    volume = item.get("search_volume", 0)
    competition = item.get("competition", "medium")
    if volume > 10000 and competition in ["low", "medium"]:
        return 5
    elif volume > 5000:
        return 4
    elif volume > 1000:
        return 3
    return 2

async def collect_competitor_data():
    """采集竞品数据"""
    try:
        for competitor in settings.COMPETITORS:
            result = await call_ahrefs_mcp("ahrefs.domain_competitors", {
                "domain": competitor,
            })
            db = SessionLocal()
            try:
                for item in result.get("competitors", [])[:5]:
                    action = CompetitorActionDB(
                        id=f"CA-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6]}",
                        competitor=competitor,
                        action_type="内容布局",
                        description=f"竞品 {competitor} 排名上升: {item.get('keyword', '')}",
                        possible_goal="提升SEO流量",
                        should_follow=False,
                        created_at=datetime.now(),
                    )
                    db.add(action)
                db.commit()
            finally:
                db.close()
    except Exception as e:
        print(f"竞品数据采集失败: {e}")