from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from knowledge_base.db import get_db, CompetitorActionDB

router = APIRouter()

@router.get("/")
async def list_competitor_actions(db: Session = Depends(get_db)):
    actions = db.query(CompetitorActionDB).order_by(CompetitorActionDB.created_at.desc()).limit(50).all()
    return actions