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