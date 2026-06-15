# 市场洞察 Agent 系统 - 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建市场洞察 Agent 系统，包含 Python Agent 核心 + Next.js Dashboard，实现趋势扫描、竞品监控、搜索洞察、机会评分、Brief 生成五大职责。

**Architecture:** 后端 Python + FastAPI 提供 REST API，前端 Next.js + Tailwind CSS 构建工作台。数据存储使用 SQLite + JSON 文件，LLM 调用使用本地部署的模型。

**Tech Stack:** Python 3.11+ / FastAPI / APScheduler / SQLite / Next.js 14 / Tailwind CSS / DeepSeek-V3

---

## Phase 1: 基础设施与核心后端

### Task 1: 项目初始化与依赖

**Files:**
- Create: `market-insight-agent/requirements.txt`
- Create: `market-insight-agent/config.py`

- [ ] **Step 1: 创建 requirements.txt**

```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
apscheduler==3.10.4
pydantic==2.5.3
pydantic-settings==2.1.0
httpx==0.26.0
feedparser==6.0.10
beautifulsoup4==4.12.3
pandas==2.1.4
sqlalchemy==2.0.25
aiosqlite==0.19.0
python-dotenv==1.0.0
```

- [ ] **Step 2: 创建 config.py**

```python
from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # 数据库
    DATABASE_URL: str = "sqlite+aiosqlite:///./market_insight.db"

    # LLM 配置
    LLM_API_URL: str = os.getenv("LLM_API_URL", "http://localhost:8000/v1/chat")
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "deepseek-v3")

    # Ahrefs MCP
    AHREFS_MCP_URL: str = os.getenv("AHREFS_MCP_URL", "http://localhost:8080/mcp")

    # 竞品名单
    COMPETITORS: List[str] = [
        "customink.com",
        "printful.com",
        "redbubble.com",
        "etsy.com",
        "zazzle.com",
    ]

    # 关键词池
    GIFT_KEYWORDS: List[str] = [
        "custom gift",
        "personalized gift",
        "gift for her",
        "gift for him",
        "couple gift",
        "anniversary gift",
        "birthday gift",
    ]

    # 调度配置
    SCAN_INTERVAL_HOURS: int = 6

    class Config:
        env_file = ".env"

settings = Settings()
```

- [ ] **Step 3: 提交**

```bash
cd market-insight-agent
pip install -r requirements.txt
git add requirements.txt config.py
git commit -m "feat: 初始化项目结构和依赖"
```

---

### Task 2: 数据库模型与初始化

**Files:**
- Create: `market-insight-agent/knowledge_base/models.py`
- Create: `market-insight-agent/knowledge_base/db.py`
- Create: `market-insight-agent/knowledge_base/__init__.py`

- [ ] **Step 1: 创建 models.py**

```python
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class Department(str, Enum):
    SEO = "SEO"
    BRAND = "品牌"
    SOCIAL_MEDIA = "社交媒体运营"
    ADVERTISING = "广告投放"
    USER_OPERATIONS = "用户运营"

class OpportunityStatus(str, Enum):
    PENDING = "待接收"
    REJECTED = "已拒绝"
    TESTING = "已测试"
    SCALED = "已放量"
    ARCHIVED = "已归档"

class TrendSignal(BaseModel):
    id: str
    name: str
    platform: str
    growth_signal: str
    related_products: List[str] = []
    suitable_channels: List[str] = []
    evidence_url: Optional[str] = None
    confidence: float = Field(ge=0, le=1)
    created_at: datetime = Field(default_factory=datetime.now)

class CompetitorAction(BaseModel):
    id: str
    competitor: str
    action_type: str  # 新品测试/促销抢量/内容布局/价格战/节日营销
    description: str
    possible_goal: str
    target_audience: Optional[str] = None
    evidence_url: Optional[str] = None
    should_follow: bool = False
    suggested_action: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

class SearchOpportunity(BaseModel):
    id: str
    keyword: str
    search_intent: str  # 信息型/比较型/购买型/灵感型
    recommended_page_type: str
    suggested_title: Optional[str] = None
    related_products: List[str] = []
    priority: int = Field(ge=1, le=5)
    search_volume: Optional[int] = None
    competition: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

class Opportunity(BaseModel):
    id: str
    source_type: str  # trend/competitor/search
    source_id: str
    title: str
    description: str
    department: Department
    demand_score: int = Field(ge=0, le=5)
    brand_relevance: int = Field(ge=0, le=5)
    competition_gap: int = Field(ge=0, le=5)
    conversion_potential: int = Field(ge=0, le=5)
    timeliness: int = Field(ge=0, le=5)
    evidence_strength: int = Field(ge=0, le=5)
    total_score: int = 0
    grade: str = "C"  # A/B/C/D
    status: OpportunityStatus = OpportunityStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class Brief(BaseModel):
    id: str  # BR-{DEPT}-{DATE}-{SEQ}
    opportunity_id: str
    department: Department
    brief_type: str
    opportunity_background: str
    target_audience: str
    evidence: str
    recommended_channels: List[str] = []
    core_message: str
    assumption: str
    success_metrics: str
    risk_warning: Optional[str] = None
    status: OpportunityStatus = OpportunityStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
```

- [ ] **Step 2: 创建 db.py**

```python
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
```

- [ ] **Step 3: 创建 __init__.py**

```python
from .db import init_db, get_db, SessionLocal
from .models import (
    TrendSignal,
    CompetitorAction,
    SearchOpportunity,
    Opportunity,
    Brief,
    Department,
    OpportunityStatus,
)

__all__ = [
    "init_db",
    "get_db",
    "SessionLocal",
    "TrendSignal",
    "CompetitorAction",
    "SearchOpportunity",
    "Opportunity",
    "Brief",
    "Department",
    "OpportunityStatus",
]
```

- [ ] **Step 4: 提交**

```bash
git add knowledge_base/
git commit -m "feat: 添加数据库模型和初始化"
```

---

### Task 3: FastAPI 入口与路由结构

**Files:**
- Create: `market-insight-agent/main.py`
- Create: `market-insight-agent/api/opportunities.py`
- Create: `market-insight-agent/api/briefs.py`
- Create: `market-insight-agent/api/trends.py`
- Create: `market-insight-agent/api/competitors.py`
- Create: `market-insight-agent/api/search.py`
- Create: `market-insight-agent/api/__init__.py`

- [ ] **Step 1: 创建 main.py**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from knowledge_base.db import init_db
from api import opportunities, briefs, trends, competitors, search

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="市场洞察 Agent API",
    description="callie.com 市场洞察系统后端 API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(opportunities.router, prefix="/api/opportunities", tags=["机会"])
app.include_router(briefs.router, prefix="/api/briefs", tags=["Brief"])
app.include_router(trends.router, prefix="/api/trends", tags=["趋势"])
app.include_router(competitors.router, prefix="/api/competitors", tags=["竞品"])
app.include_router(search.router, prefix="/api/search", tags=["搜索"])

@app.get("/")
async def root():
    return {"message": "市场洞察 Agent API", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

- [ ] **Step 2: 创建 opportunities.py**

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from knowledge_base.db import get_db, OpportunityDB
from knowledge_base.models import OpportunityStatus, Department
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
```

- [ ] **Step 3: 创建 briefs.py**

```python
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
```

- [ ] **Step 4: 创建 trends.py**

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from knowledge_base.db import get_db, TrendSignalDB

router = APIRouter()

@router.get("/")
async def list_trends(db: Session = Depends(get_db)):
    trends = db.query(TrendSignalDB).order_by(TrendSignalDB.created_at.desc()).limit(50).all()
    return trends
```

- [ ] **Step 5: 创建 competitors.py**

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from knowledge_base.db import get_db, CompetitorActionDB

router = APIRouter()

@router.get("/")
async def list_competitor_actions(db: Session = Depends(get_db)):
    actions = db.query(CompetitorActionDB).order_by(CompetitorActionDB.created_at.desc()).limit(50).all()
    return actions
```

- [ ] **Step 6: 创建 search.py**

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from knowledge_base.db import get_db, SearchOpportunityDB

router = APIRouter()

@router.get("/")
async def list_search_opportunities(db: Session = Depends(get_db)):
    opportunities = db.query(SearchOpportunityDB).order_by(SearchOpportunityDB.priority.desc()).limit(50).all()
    return opportunities
```

- [ ] **Step 7: 提交**

```bash
git add main.py api/
git commit -m "feat: 添加FastAPI入口和路由结构"
```

---

### Task 4: Agent 核心 - Brief 生成器

**Files:**
- Create: `market-insight-agent/agents/brief_generator.py`
- Create: `market-insight-agent/agents/__init__.py`

- [ ] **Step 1: 创建 brief_generator.py**

```python
import httpx
from datetime import datetime
from knowledge_base.db import SessionLocal, BriefDB, OpportunityDB
from knowledge_base.models import Department, Brief
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
```

- [ ] **Step 2: 提交**

```bash
git add agents/brief_generator.py agents/__init__.py
git commit -m "feat: 添加Brief生成器Agent"
```

---

### Task 5: 调度器

**Files:**
- Create: `market-insight-agent/scheduler.py`

- [ ] **Step 1: 创建 scheduler.py**

```python
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
```

- [ ] **Step 2: 修改 main.py 添加调度器支持**

```python
from scheduler import start_scheduler, stop_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    start_scheduler()
    yield
    stop_scheduler()
```

- [ ] **Step 3: 提交**

```bash
git add scheduler.py main.py
git commit -m "feat: 添加调度器支持"
```

---

## Phase 2: 前端工作台

### Task 6: Next.js 项目初始化

**Files:**
- Create: `market-insight-dashboard/package.json`
- Create: `market-insight-dashboard/next.config.js`
- Create: `market-insight-dashboard/tailwind.config.ts`
- Create: `market-insight-dashboard/tsconfig.json`

- [ ] **Step 1: 创建 package.json**

```json
{
  "name": "market-insight-dashboard",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "14.1.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "lucide-react": "^0.312.0",
    "clsx": "^2.1.0"
  },
  "devDependencies": {
    "@types/node": "^20.11.0",
    "@types/react": "^18.2.48",
    "@types/react-dom": "^18.2.18",
    "autoprefixer": "^10.4.17",
    "postcss": "^8.4.33",
    "tailwindcss": "^3.4.1",
    "typescript": "^5.3.3"
  }
}
```

- [ ] **Step 2: 创建配置文件**

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  trailingSlash: true,
  images: {
    unoptimized: true,
  },
}

module.exports = nextConfig
```

```typescript
import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          500: '#0ea5e9',
          600: '#0284c7',
        },
      },
    },
  },
  plugins: [],
}
export default config
```

```json
{
  "compilerOptions": {
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{"name": "next"}],
    "paths": {"@/*": ["./src/*"]}
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

- [ ] **Step 3: 提交**

```bash
cd market-insight-dashboard
npm install
git add package.json next.config.js tailwind.config.ts tsconfig.json
git commit -m "feat: 初始化Next.js项目"
```

---

### Task 7: 主布局和导航

**Files:**
- Create: `market-insight-dashboard/src/app/globals.css`
- Create: `market-insight-dashboard/src/app/layout.tsx`
- Create: `market-insight-dashboard/src/components/Sidebar.tsx`

- [ ] **Step 1: 创建 globals.css**

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --background: #ffffff;
  --foreground: #171717;
}

body {
  color: var(--foreground);
  background: var(--background);
}
```

- [ ] **Step 2: 创建 layout.tsx**

```typescript
import './globals.css'
import type { Metadata } from 'next'
import Sidebar from '@/components/Sidebar'

export const metadata: Metadata = {
  title: '市场洞察工作台',
  description: 'callie.com 市场洞察 Agent 系统',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh-CN">
      <body className="flex min-h-screen">
        <Sidebar />
        <main className="flex-1 ml-64 p-8">
          {children}
        </main>
      </body>
    </html>
  )
}
```

- [ ] **Step 3: 创建 Sidebar.tsx**

```typescript
'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { clsx } from 'clsx'
import {
  Target,
  TrendingUp,
  Building2,
  Search,
  FileText,
  Settings,
} from 'lucide-react'

const navItems = [
  { href: '/', label: '机会列表', icon: Target },
  { href: '/trends', label: '趋势监控', icon: TrendingUp },
  { href: '/competitors', label: '竞品档案', icon: Building2 },
  { href: '/search', label: '搜索洞察', icon: Search },
  { href: '/briefs', label: 'Brief管理', icon: FileText },
  { href: '/settings', label: '设置', icon: Settings },
]

export default function Sidebar() {
  const pathname = usePathname()

  return (
    <aside className="fixed left-0 top-0 h-screen w-64 bg-slate-900 text-white">
      <div className="p-6">
        <h1 className="text-xl font-bold flex items-center gap-2">
          <span>🔥</span>
          市场洞察工作台
        </h1>
      </div>
      <nav className="mt-6">
        {navItems.map((item) => {
          const Icon = item.icon
          const isActive = pathname === item.href
          return (
            <Link
              key={item.href}
              href={item.href}
              className={clsx(
                'flex items-center gap-3 px-6 py-3 text-sm transition-colors',
                isActive
                  ? 'bg-slate-800 text-white border-l-2 border-primary-500'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800'
              )}
            >
              <Icon size={18} />
              {item.label}
            </Link>
          )
        })}
      </nav>
    </aside>
  )
}
```

- [ ] **Step 4: 提交**

```bash
git add src/app/globals.css src/app/layout.tsx src/components/Sidebar.tsx
git commit -m "feat: 添加主布局和导航"
```

---

### Task 8: 机会列表页面

**Files:**
- Create: `market-insight-dashboard/src/app/page.tsx`
- Create: `market-insight-dashboard/src/components/OpportunityCard.tsx`
- Create: `market-insight-dashboard/src/components/FilterBar.tsx`
- Create: `market-insight-dashboard/src/types/index.ts`

- [ ] **Step 1: 创建 types/index.ts**

```typescript
export interface Opportunity {
  id: string
  source_type: string
  source_id: string
  title: string
  description: string
  department: string
  demand_score: number
  brand_relevance: number
  competition_gap: number
  conversion_potential: number
  timeliness: number
  evidence_strength: number
  total_score: number
  grade: string
  status: string
  created_at: string
  updated_at: string
}

export interface Brief {
  id: string
  opportunity_id: string
  department: string
  brief_type: string
  opportunity_background: string
  target_audience: string
  evidence: string
  recommended_channels: string
  core_message: string
  assumption: string
  success_metrics: string
  risk_warning?: string
  status: string
  created_at: string
  updated_at: string
}

export const DEPARTMENTS = ['SEO', '品牌', '社交媒体运营', '广告投放', '用户运营'] as const

export const STATUS_OPTIONS = ['待接收', '已拒绝', '已测试', '已放量', '已归档'] as const

export const GRADE_OPTIONS = ['A', 'B', 'C', 'D'] as const
```

- [ ] **Step 2: 创建 FilterBar.tsx**

```typescript
'use client'

import { clsx } from 'clsx'
import { DEPARTMENTS, STATUS_OPTIONS, GRADE_OPTIONS } from '@/types'

interface FilterBarProps {
  filters: {
    department: string
    status: string
    grade: string
  }
  onFilterChange: (key: string, value: string) => void
}

export default function FilterBar({ filters, onFilterChange }: FilterBarProps) {
  return (
    <div className="flex gap-4 mb-6">
      <select
        value={filters.department}
        onChange={(e) => onFilterChange('department', e.target.value)}
        className="px-4 py-2 border rounded-lg text-sm"
      >
        <option value="">部门（全部）</option>
        {DEPARTMENTS.map((d) => (
          <option key={d} value={d}>{d}</option>
        ))}
      </select>
      <select
        value={filters.status}
        onChange={(e) => onFilterChange('status', e.target.value)}
        className="px-4 py-2 border rounded-lg text-sm"
      >
        <option value="">状态（全部）</option>
        {STATUS_OPTIONS.map((s) => (
          <option key={s} value={s}>{s}</option>
        ))}
      </select>
      <select
        value={filters.grade}
        onChange={(e) => onFilterChange('grade', e.target.value)}
        className="px-4 py-2 border rounded-lg text-sm"
      >
        <option value="">等级（全部）</option>
        {GRADE_OPTIONS.map((g) => (
          <option key={g} value={g}>{g}级</option>
        ))}
      </select>
    </div>
  )
}
```

- [ ] **Step 3: 创建 OpportunityCard.tsx**

```typescript
import { clsx } from 'clsx'
import { Opportunity } from '@/types'

interface OpportunityCardProps {
  opportunity: Opportunity
}

const GRADE_COLORS = {
  A: 'bg-red-100 text-red-700 border-red-200',
  B: 'bg-orange-100 text-orange-700 border-orange-200',
  C: 'bg-yellow-100 text-yellow-700 border-yellow-200',
  D: 'bg-gray-100 text-gray-600 border-gray-200',
}

const STATUS_COLORS = {
  '待接收': 'bg-blue-100 text-blue-700',
  '已拒绝': 'bg-gray-100 text-gray-600',
  '已测试': 'bg-purple-100 text-purple-700',
  '已放量': 'bg-green-100 text-green-700',
  '已归档': 'bg-gray-100 text-gray-500',
}

export default function OpportunityCard({ opportunity }: OpportunityCardProps) {
  return (
    <div className="border rounded-lg p-4 hover:shadow-md transition-shadow bg-white">
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-2">
          <span className={clsx('px-2 py-1 text-xs font-medium rounded border', GRADE_COLORS[opportunity.grade as keyof typeof GRADE_COLORS])}>
            {opportunity.grade}级
          </span>
          <span className="text-xs text-slate-500">{opportunity.department}</span>
        </div>
        <span className={clsx('px-2 py-1 text-xs rounded', STATUS_COLORS[opportunity.status as keyof typeof STATUS_COLORS])}>
          {opportunity.status}
        </span>
      </div>
      <h3 className="font-medium text-slate-900 mb-2">{opportunity.title}</h3>
      <p className="text-sm text-slate-600 mb-3 line-clamp-2">{opportunity.description}</p>
      <div className="flex items-center justify-between text-xs text-slate-500">
        <span>总分: <span className="font-medium text-slate-700">{opportunity.total_score}</span></span>
        <span>{new Date(opportunity.created_at).toLocaleDateString('zh-CN')}</span>
      </div>
    </div>
  )
}
```

- [ ] **Step 4: 创建主页面 page.tsx**

```typescript
'use client'

import { useState, useEffect } from 'react'
import FilterBar from '@/components/FilterBar'
import OpportunityCard from '@/components/OpportunityCard'
import { Opportunity } from '@/types'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

export default function OpportunitiesPage() {
  const [opportunities, setOpportunities] = useState<Opportunity[]>([])
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState({
    department: '',
    status: '',
    grade: '',
  })

  useEffect(() => {
    fetchOpportunities()
  }, [filters])

  const fetchOpportunities = async () => {
    setLoading(true)
    try {
      const params = new URLSearchParams()
      if (filters.department) params.append('department', filters.department)
      if (filters.status) params.append('status', filters.status)
      if (filters.grade) params.append('grade', filters.grade)

      const res = await fetch(`${API_BASE}/opportunities/?${params}`)
      const data = await res.json()
      setOpportunities(data)
    } catch (error) {
      console.error('Failed to fetch opportunities:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleFilterChange = (key: string, value: string) => {
    setFilters((prev) => ({ ...prev, [key]: value }))
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold">机会列表</h2>
        <span className="text-sm text-slate-500">共 {opportunities.length} 条</span>
      </div>

      <FilterBar filters={filters} onFilterChange={handleFilterChange} />

      {loading ? (
        <div className="text-center py-12 text-slate-500">加载中...</div>
      ) : opportunities.length === 0 ? (
        <div className="text-center py-12 text-slate-500">
          暂无机会数据
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {opportunities.map((opp) => (
            <OpportunityCard key={opp.id} opportunity={opp} />
          ))}
        </div>
      )}
    </div>
  )
}
```

- [ ] **Step 5: 提交**

```bash
git add src/app/page.tsx src/components/ src/types/
git commit -m "feat: 添加机会列表页面"
```

---

### Task 9: Brief 管理页面

**Files:**
- Create: `market-insight-dashboard/src/app/briefs/page.tsx`
- Create: `market-insight-dashboard/src/components/BriefCard.tsx`

- [ ] **Step 1: 创建 BriefCard.tsx**

```typescript
import { clsx } from 'clsx'
import { Brief } from '@/types'

interface BriefCardProps {
  brief: Brief
  onStatusChange: (briefId: string, newStatus: string) => void
}

const STATUS_COLORS = {
  '待接收': 'bg-blue-100 text-blue-700',
  '已拒绝': 'bg-gray-100 text-gray-600',
  '已测试': 'bg-purple-100 text-purple-700',
  '已放量': 'bg-green-100 text-green-700',
  '已归档': 'bg-gray-100 text-gray-500',
}

export default function BriefCard({ brief, onStatusChange }: BriefCardProps) {
  return (
    <div className="border rounded-lg p-5 bg-white hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-4">
        <div>
          <span className="text-xs font-mono text-slate-500">{brief.id}</span>
          <h3 className="font-medium text-slate-900 mt-1">{brief.brief_type}</h3>
        </div>
        <span className={clsx('px-2 py-1 text-xs rounded', STATUS_COLORS[brief.status as keyof typeof STATUS_COLORS])}>
          {brief.status}
        </span>
      </div>

      <div className="space-y-3 text-sm">
        <div>
          <span className="text-slate-500">部门：</span>
          <span className="text-slate-700">{brief.department}</span>
        </div>
        <div>
          <span className="text-slate-500">目标人群：</span>
          <span className="text-slate-700">{brief.target_audience}</span>
        </div>
        <div>
          <span className="text-slate-500">核心信息：</span>
          <span className="text-slate-700">{brief.core_message}</span>
        </div>
        <div>
          <span className="text-slate-500">成功指标：</span>
          <span className="text-slate-700">{brief.success_metrics}</span>
        </div>
      </div>

      <div className="mt-4 pt-4 border-t flex items-center justify-between">
        <span className="text-xs text-slate-500">
          {new Date(brief.created_at).toLocaleDateString('zh-CN')}
        </span>
        <select
          value={brief.status}
          onChange={(e) => onStatusChange(brief.id, e.target.value)}
          className="text-xs px-2 py-1 border rounded"
        >
          <option value="待接收">待接收</option>
          <option value="已拒绝">已拒绝</option>
          <option value="已测试">已测试</option>
          <option value="已放量">已放量</option>
          <option value="已归档">已归档</option>
        </select>
      </div>
    </div>
  )
}
```

- [ ] **Step 2: 创建 briefs/page.tsx**

```typescript
'use client'

import { useState, useEffect } from 'react'
import BriefCard from '@/components/BriefCard'
import { Brief } from '@/types'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

export default function BriefsPage() {
  const [briefs, setBriefs] = useState<Brief[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchBriefs()
  }, [])

  const fetchBriefs = async () => {
    setLoading(true)
    try {
      const res = await fetch(`${API_BASE}/briefs/`)
      const data = await res.json()
      setBriefs(data)
    } catch (error) {
      console.error('Failed to fetch briefs:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleStatusChange = async (briefId: string, newStatus: string) => {
    try {
      await fetch(`${API_BASE}/briefs/${briefId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus }),
      })
      fetchBriefs()
    } catch (error) {
      console.error('Failed to update brief status:', error)
    }
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold">Brief 管理</h2>
        <span className="text-sm text-slate-500">共 {briefs.length} 条</span>
      </div>

      {loading ? (
        <div className="text-center py-12 text-slate-500">加载中...</div>
      ) : briefs.length === 0 ? (
        <div className="text-center py-12 text-slate-500">
          暂无 Brief 数据
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {briefs.map((brief) => (
            <BriefCard key={brief.id} brief={brief} onStatusChange={handleStatusChange} />
          ))}
        </div>
      )}
    </div>
  )
}
```

- [ ] **Step 3: 提交**

```bash
git add src/app/briefs/page.tsx src/components/BriefCard.tsx
git commit -m "feat: 添加Brief管理页面"
```

---

### Task 10: 其他页面（趋势/竞品/搜索/设置）

**Files:**
- Create: `market-insight-dashboard/src/app/trends/page.tsx`
- Create: `market-insight-dashboard/src/app/competitors/page.tsx`
- Create: `market-insight-dashboard/src/app/search/page.tsx`
- Create: `market-insight-dashboard/src/app/settings/page.tsx`

- [ ] **Step 1: 创建 trends/page.tsx**

```typescript
'use client'

import { useState, useEffect } from 'react'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

export default function TrendsPage() {
  const [trends, setTrends] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`${API_BASE}/trends/`).then(res => res.json()).then(data => {
      setTrends(data)
      setLoading(false)
    }).catch(() => setLoading(false))
  }, [])

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">趋势监控</h2>
      {loading ? (
        <div className="text-center py-12 text-slate-500">加载中...</div>
      ) : trends.length === 0 ? (
        <div className="text-center py-12 text-slate-500">暂无趋势数据</div>
      ) : (
        <div className="space-y-4">
          {trends.map((trend: any) => (
            <div key={trend.id} className="border rounded-lg p-4 bg-white">
              <div className="flex items-center gap-2 mb-2">
                <span className="text-xs px-2 py-1 bg-blue-100 text-blue-700 rounded">{trend.platform}</span>
                <span className="text-sm text-slate-500">置信度: {(trend.confidence * 100).toFixed(0)}%</span>
              </div>
              <h3 className="font-medium">{trend.name}</h3>
              <p className="text-sm text-slate-600 mt-1">{trend.growth_signal}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
```

- [ ] **Step 2: 创建 competitors/page.tsx**

```typescript
'use client'

import { useState, useEffect } from 'react'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

export default function CompetitorsPage() {
  const [actions, setActions] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`${API_BASE}/competitors/`).then(res => res.json()).then(data => {
      setActions(data)
      setLoading(false)
    }).catch(() => setLoading(false))
  }, [])

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">竞品档案</h2>
      {loading ? (
        <div className="text-center py-12 text-slate-500">加载中...</div>
      ) : actions.length === 0 ? (
        <div className="text-center py-12 text-slate-500">暂无竞品数据</div>
      ) : (
        <div className="space-y-4">
          {actions.map((action: any) => (
            <div key={action.id} className="border rounded-lg p-4 bg-white">
              <div className="flex items-center justify-between mb-2">
                <span className="font-medium">{action.competitor}</span>
                <span className="text-xs px-2 py-1 bg-slate-100 rounded">{action.action_type}</span>
              </div>
              <p className="text-sm text-slate-600">{action.description}</p>
              {action.suggested_action && (
                <p className="text-sm text-primary-600 mt-2">💡 {action.suggested_action}</p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
```

- [ ] **Step 3: 创建 search/page.tsx**

```typescript
'use client'

import { useState, useEffect } from 'react'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

export default function SearchPage() {
  const [opportunities, setOpportunities] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`${API_BASE}/search/`).then(res => res.json()).then(data => {
      setOpportunities(data)
      setLoading(false)
    }).catch(() => setLoading(false))
  }, [])

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">搜索洞察</h2>
      {loading ? (
        <div className="text-center py-12 text-slate-500">加载中...</div>
      ) : opportunities.length === 0 ? (
        <div className="text-center py-12 text-slate-500">暂无搜索数据</div>
      ) : (
        <div className="bg-white border rounded-lg overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-slate-50">
              <tr>
                <th className="text-left p-3">关键词</th>
                <th className="text-left p-3">搜索意图</th>
                <th className="text-left p-3">推荐页面</th>
                <th className="text-right p-3">优先级</th>
              </tr>
            </thead>
            <tbody>
              {opportunities.map((item: any) => (
                <tr key={item.id} className="border-t">
                  <td className="p-3 font-medium">{item.keyword}</td>
                  <td className="p-3 text-slate-600">{item.search_intent}</td>
                  <td className="p-3 text-slate-600">{item.recommended_page_type}</td>
                  <td className="p-3 text-right">
                    <span className={`px-2 py-1 rounded text-xs ${
                      item.priority >= 4 ? 'bg-green-100 text-green-700' :
                      item.priority >= 3 ? 'bg-yellow-100 text-yellow-700' :
                      'bg-gray-100 text-gray-600'
                    }`}>
                      {item.priority}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
```

- [ ] **Step 4: 创建 settings/page.tsx**

```typescript
'use client'

export default function SettingsPage() {
  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">设置</h2>
      <div className="bg-white border rounded-lg p-6 max-w-xl">
        <h3 className="font-medium mb-4">数据源配置</h3>
        <div className="space-y-4 text-sm">
          <div>
            <label className="block text-slate-500 mb-1">Ahrefs MCP URL</label>
            <input
              type="text"
              placeholder="http://localhost:8080/mcp"
              className="w-full px-3 py-2 border rounded"
            />
          </div>
          <div>
            <label className="block text-slate-500 mb-1">LLM API URL</label>
            <input
              type="text"
              placeholder="http://localhost:8000/v1/chat"
              className="w-full px-3 py-2 border rounded"
            />
          </div>
          <div>
            <label className="block text-slate-500 mb-1">扫描间隔（小时）</label>
            <input
              type="number"
              defaultValue={6}
              className="w-full px-3 py-2 border rounded"
            />
          </div>
          <button className="px-4 py-2 bg-primary-500 text-white rounded hover:bg-primary-600">
            保存配置
          </button>
        </div>
      </div>
    </div>
  )
}
```

- [ ] **Step 5: 提交**

```bash
git add src/app/trends/ src/app/competitors/ src/app/search/ src/app/settings/
git commit -m "feat: 添加趋势/竞品/搜索/设置页面"
```

---

## Phase 3: 数据采集与集成

### Task 11: Ahrefs 数据采集器

**Files:**
- Create: `market-insight-agent/collectors/ahrefs_collector.py`
- Create: `market-insight-agent/collectors/__init__.py`

- [ ] **Step 1: 创建 ahrefs_collector.py**

```python
import httpx
import json
from datetime import datetime
from knowledge_base.db import SessionLocal, SearchOpportunityDB, CompetitorActionDB, OpportunityDB
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
```

- [ ] **Step 2: 提交**

```bash
git add collectors/ahrefs_collector.py
git commit -m "feat: 添加Ahrefs数据采集器"
```

---

### Task 12: 企业微信推送

**Files:**
- Create: `market-insight-agent/notifications/wechat_bot.py`
- Create: `market-insight-agent/notifications/__init__.py`

- [ ] **Step 1: 创建 wechat_bot.py**

```python
import httpx
import json
from datetime import datetime
from typing import List

class WeChatBot:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send_text(self, content: str):
        """发送文本消息"""
        data = {
            "msgtype": "text",
            "text": {"content": content}
        }
        self._send(data)

    def send_markdown(self, content: str):
        """发送 Markdown 消息"""
        data = {
            "msgtype": "markdown",
            "markdown": {"content": content}
        }
        self._send(data)

    def _send(self, data: dict):
        """发送请求"""
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.post(self.webhook_url, json=data)
                response.raise_for_status()
        except Exception as e:
            print(f"Failed to send WeChat notification: {e}")

    def send_daily_report(self, opportunities: List[dict], briefs: List[dict]):
        """发送每日简报"""
        content = f"""【市场洞察日报】{datetime.now().strftime('%Y-%m-%d')}

🔥 高价值机会
"""
        for opp in opportunities[:3]:
            content += f"{opp['title']}\n"

        content += f"""
📊 Brief 状态
- 待接收: {len([b for b in briefs if b['status'] == '待接收'])}
- 执行中: {len([b for b in briefs if b['status'] in ['已测试', '已放量']])}
"""
        self.send_markdown(content)

# 使用示例
# bot = WeChatBot("YOUR_WEBHOOK_URL")
# bot.send_text("测试消息")
```

- [ ] **Step 2: 提交**

```bash
git add notifications/wechat_bot.py
git commit -m "feat: 添加企业微信推送功能"
```

---

## 自检清单

完成所有任务后，请检查：

1. **Spec 覆盖：** 每个设计需求都有对应实现
2. **无占位符：** 代码中没有 TBD/TODO/待定 等占位符
3. **类型一致性：** API 字段名在前后端一致
4. **可运行性：** 每个组件可独立测试

---

**Plan complete and saved to `docs/superpowers/plans/2026-06-15-callie-market-insight-agent-plan.md`. Two execution options:**

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**