from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from knowledge_base.db import get_db, OpportunityDB
from datetime import datetime

router = APIRouter()

class OpportunityResponse(BaseModel):
    id: str
    source_type: str
    source_id: str
    title: str
    description: str
    department: str
    demand_score: int
    brand_relevance: int
    competition_gap: int
    conversion_potential: int
    timeliness: int
    evidence_strength: int
    total_score: int
    grade: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class OpportunityUpdate(BaseModel):
    status: Optional[str] = None
    grade: Optional[str] = None

@router.get("/", response_model=List[OpportunityResponse])
async def list_opportunities(
    department: Optional[str] = None,
    status: Optional[str] = None,
    grade: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(OpportunityDB)
    if department:
        query = query.filter(OpportunityDB.department == department)
    if status:
        query = query.filter(OpportunityDB.status == status)
    if grade:
        query = query.filter(OpportunityDB.grade == grade)
    opportunities = query.order_by(OpportunityDB.total_score.desc()).all()
    return opportunities

@router.get("/{opportunity_id}", response_model=OpportunityResponse)
async def get_opportunity(opportunity_id: str, db: Session = Depends(get_db)):
    opportunity = db.query(OpportunityDB).filter(OpportunityDB.id == opportunity_id).first()
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return opportunity

@router.patch("/{opportunity_id}", response_model=OpportunityResponse)
async def update_opportunity(
    opportunity_id: str,
    update: OpportunityUpdate,
    db: Session = Depends(get_db),
):
    opportunity = db.query(OpportunityDB).filter(OpportunityDB.id == opportunity_id).first()
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    if update.status:
        opportunity.status = update.status
    if update.grade:
        opportunity.grade = update.grade
    opportunity.updated_at = datetime.now()
    db.commit()
    db.refresh(opportunity)
    return opportunity