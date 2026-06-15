from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from knowledge_base.db import get_db, CompetitorActionDB, CompetitorDB

router = APIRouter()

class CompetitorResponse(BaseModel):
    id: str
    brand: str
    url: Optional[str]
    category: Optional[str]
    has_custom_product: Optional[str]
    marketing_email: Optional[str]
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class CompetitorActionResponse(BaseModel):
    id: str
    competitor: str
    action_type: str
    description: str
    possible_goal: Optional[str]
    target_audience: Optional[str]
    evidence_url: Optional[str]
    should_follow: bool
    suggested_action: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

@router.get("/", response_model=List[CompetitorResponse])
async def list_competitors(
    category: Optional[str] = None,
    has_custom: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """查询竞品清单（96条已导入）"""
    query = db.query(CompetitorDB)
    if category:
        query = query.filter(CompetitorDB.category.contains(category))
    if has_custom:
        query = query.filter(CompetitorDB.has_custom_product.contains(has_custom))
    competitors = query.order_by(CompetitorDB.created_at.desc()).all()
    return competitors

@router.get("/actions/", response_model=List[CompetitorActionResponse])
async def list_competitor_actions(db: Session = Depends(get_db)):
    """查询竞品动态"""
    actions = db.query(CompetitorActionDB).order_by(CompetitorActionDB.created_at.desc()).limit(50).all()
    return actions