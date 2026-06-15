from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import logging

from agents.brief_generator import create_brief_from_opportunity
from knowledge_base.db import SessionLocal, OpportunityDB

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()

async def score_and_generate_briefs():
    """扫描待处理的机会，生成Brief"""
    db = SessionLocal()
    try:
        # 查找 A 级机会（总分 >= 25）且尚未生成 Brief
        opportunities = db.query(OpportunityDB).filter(
            OpportunityDB.total_score >= 25,
            OpportunityDB.status == "待接收"
        ).all()

        for opp in opportunities:
            try:
                brief_id = await create_brief_from_opportunity(opp.id)
                logger.info(f"为机会 {opp.id} 生成 Brief: {brief_id}")
            except Exception as e:
                logger.error(f"生成 Brief 失败: {e}")
    finally:
        db.close()

def start_scheduler():
    # 每6小时执行一次机会扫描和Brief生成
    scheduler.add_job(
        score_and_generate_briefs,
        trigger=IntervalTrigger(hours=6),
        id="score_and_briefs",
        name="机会评分与Brief生成",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("调度器已启动")

def stop_scheduler():
    scheduler.shutdown()
    logger.info("调度器已停止")