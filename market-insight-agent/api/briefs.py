from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from knowledge_base.db import get_db, BriefDB
from datetime import datetime

router = APIRouter()

class BriefResponse(BaseModel):
    id: str
    opportunity_id: str
    department: str
    brief_type: str
    opportunity_background: str
    target_audience: str
    evidence: str
    recommended_channels: str
    core_message: str
    assumption: str
    success_metrics: str
    risk_warning: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class BriefUpdate(BaseModel):
    status: Optional[str] = None

@router.get("/", response_model=List[BriefResponse])
async def list_briefs(
    department: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(BriefDB)
    if department:
        query = query.filter(BriefDB.department == department)
    if status:
        query = query.filter(BriefDB.status == status)
    briefs = query.order_by(BriefDB.created_at.desc()).all()
    return briefs

@router.get("/{brief_id}", response_model=BriefResponse)
async def get_brief(brief_id: str, db: Session = Depends(get_db)):
    brief = db.query(BriefDB).filter(BriefDB.id == brief_id).first()
    if not brief:
        raise HTTPException(status_code=404, detail="Brief not found")
    return brief

@router.patch("/{brief_id}", response_model=BriefResponse)
async def update_brief(
    brief_id: str,
    update: BriefUpdate,
    db: Session = Depends(get_db),
):
    brief = db.query(BriefDB).filter(BriefDB.id == brief_id).first()
    if not brief:
        raise HTTPException(status_code=404, detail="Brief not found")
    if update.status:
        brief.status = update.status
    brief.updated_at = datetime.now()
    db.commit()
    db.refresh(brief)
    return brief