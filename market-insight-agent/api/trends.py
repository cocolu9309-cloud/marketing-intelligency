from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from knowledge_base.db import get_db, TrendSignalDB

router = APIRouter()

@router.get("/")
async def list_trends(db: Session = Depends(get_db)):
    trends = db.query(TrendSignalDB).order_by(TrendSignalDB.created_at.desc()).limit(50).all()
    return trends