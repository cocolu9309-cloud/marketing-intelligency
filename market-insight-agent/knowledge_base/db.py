from sqlalchemy import create_engine, Column, String, Integer, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import json

DATABASE_URL = "sqlite:///./market_insight.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class TrendSignalDB(Base):
    __tablename__ = "trend_signals"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    growth_signal = Column(Text, nullable=False)
    related_products = Column(Text)  # JSON
    suitable_channels = Column(Text)  # JSON
    evidence_url = Column(String)
    confidence = Column(Float, default=0.5)
    created_at = Column(DateTime, default=datetime.now)


class CompetitorActionDB(Base):
    __tablename__ = "competitor_actions"
    id = Column(String, primary_key=True)
    competitor = Column(String, nullable=False)
    action_type = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    possible_goal = Column(Text)
    target_audience = Column(String)
    evidence_url = Column(String)
    should_follow = Column(Boolean, default=False)
    suggested_action = Column(Text)
    created_at = Column(DateTime, default=datetime.now)


class SearchOpportunityDB(Base):
    __tablename__ = "search_opportunities"
    id = Column(String, primary_key=True)
    keyword = Column(String, nullable=False)
    search_intent = Column(String, nullable=False)
    recommended_page_type = Column(String)
    suggested_title = Column(String)
    related_products = Column(Text)  # JSON
    priority = Column(Integer, default=3)
    search_volume = Column(Integer)
    competition = Column(String)
    created_at = Column(DateTime, default=datetime.now)


class OpportunityDB(Base):
    __tablename__ = "opportunities"
    id = Column(String, primary_key=True)
    source_type = Column(String, nullable=False)
    source_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    department = Column(String, nullable=False)
    demand_score = Column(Integer, default=3)
    brand_relevance = Column(Integer, default=3)
    competition_gap = Column(Integer, default=3)
    conversion_potential = Column(Integer, default=3)
    timeliness = Column(Integer, default=3)
    evidence_strength = Column(Integer, default=3)
    total_score = Column(Integer, default=0)
    grade = Column(String, default="C")
    status = Column(String, default="待接收")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)


class BriefDB(Base):
    __tablename__ = "briefs"
    id = Column(String, primary_key=True)
    opportunity_id = Column(String, ForeignKey("opportunities.id"))
    department = Column(String, nullable=False)
    brief_type = Column(String, nullable=False)
    opportunity_background = Column(Text, nullable=False)
    target_audience = Column(String, nullable=False)
    evidence = Column(Text, nullable=False)
    recommended_channels = Column(Text)  # JSON
    core_message = Column(Text, nullable=False)
    assumption = Column(Text, nullable=False)
    success_metrics = Column(Text, nullable=False)
    risk_warning = Column(Text)
    status = Column(String, default="待接收")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()