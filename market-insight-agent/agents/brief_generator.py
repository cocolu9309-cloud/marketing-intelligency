import httpx
from datetime import datetime
from knowledge_base.db import SessionLocal, BriefDB, OpportunityDB
from config import settings
import json
import uuid

BRIEF_SEQ = 1

def generate_brief_id(department: str) -> str:
    global BRIEF_SEQ
    today = datetime.now().strftime("%Y%m%d")
    bid = f"BR-{department[:3].upper()}-{today}-{BRIEF_SEQ:03d}"
    BRIEF_SEQ += 1
    return bid

async def call_llm(prompt: str) -> str:
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                settings.LLM_API_URL,
                json={
                    "model": settings.LLM_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                },
                headers={"Authorization": f"Bearer {settings.LLM_API_KEY}"} if settings.LLM_API_KEY else {},
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"LLM调用失败: {str(e)}"

async def generate_brief_from_opportunity(opportunity: dict) -> dict:
    prompt = f"""
基于以下机会信息，生成一个标准化的营销 Brief：

机会信息：
- 标题：{opportunity['title']}
- 描述：{opportunity['description']}
- 来源：{opportunity['source_type']}
- 部门：{opportunity['department']}
- 总分：{opportunity['total_score']}

请生成以下字段（JSON格式）：
- brief_type: Brief类型（如：热点借势、关键词优化、测试等）
- opportunity_background: 机会背景（50字内）
- target_audience: 目标人群（30字内）
- evidence: 证据（支持你决策的关键数据或事实，50字内）
- recommended_channels: 推荐渠道（数组，如：["TikTok", "Instagram"]）
- core_message: 核心信息（这次营销要传达的关键信息，30字内）
- assumption: 假设（我们预期什么，会什么有效，30字内）
- success_metrics: 成功指标（可量化的指标，40字内）
- risk_warning: 风险提示（如无风险则填"无"）

只返回JSON，不要有其他内容。
"""
    llm_response = await call_llm(prompt)
    try:
        brief_data = json.loads(llm_response)
        return brief_data
    except:
        return {
            "brief_type": "待定",
            "opportunity_background": opportunity.get("description", "")[:50],
            "target_audience": "待定",
            "evidence": "待补充",
            "recommended_channels": ["待定"],
            "core_message": "待定",
            "assumption": "待定",
            "success_metrics": "待定",
            "risk_warning": "待定",
        }

async def create_brief_from_opportunity(opportunity_id: str) -> str:
    db = SessionLocal()
    try:
        opp = db.query(OpportunityDB).filter(OpportunityDB.id == opportunity_id).first()
        if not opp:
            raise ValueError(f"Opportunity {opportunity_id} not found")

        opp_dict = {
            "title": opp.title,
            "description": opp.description,
            "source_type": opp.source_type,
            "department": opp.department,
            "total_score": opp.total_score,
        }

        brief_data = await generate_brief_from_opportunity(opp_dict)
        brief_id = generate_brief_id(opp.department)

        brief = BriefDB(
            id=brief_id,
            opportunity_id=opportunity_id,
            department=opp.department,
            brief_type=brief_data.get("brief_type", "待定"),
            opportunity_background=brief_data.get("opportunity_background", ""),
            target_audience=brief_data.get("target_audience", ""),
            evidence=brief_data.get("evidence", ""),
            recommended_channels=json.dumps(brief_data.get("recommended_channels", [])),
            core_message=brief_data.get("core_message", ""),
            assumption=brief_data.get("assumption", ""),
            success_metrics=brief_data.get("success_metrics", ""),
            risk_warning=brief_data.get("risk_warning", ""),
            status="待接收",
        )
        db.add(brief)
        db.commit()
        return brief_id
    finally:
        db.close()