from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from knowledge_base.db import get_db, SearchOpportunityDB

router = APIRouter()

@router.get("/")
async def list_search_opportunities(db: Session = Depends(get_db)):
    opportunities = db.query(SearchOpportunityDB).order_by(SearchOpportunityDB.priority.desc()).limit(50).all()
    return opportunities