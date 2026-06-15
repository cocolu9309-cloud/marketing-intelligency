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