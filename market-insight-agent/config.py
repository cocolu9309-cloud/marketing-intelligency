from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # 数据库
    DATABASE_URL: str = "sqlite+aiosqlite:///./market_insight.db"

    # LLM 配置
    LLM_API_URL: str = "http://localhost:8000/v1/chat"
    LLM_API_KEY: str = ""
    LLM_MODEL: str = "deepseek-chat"

    # Ahrefs MCP
    AHREFS_MCP_URL: str = "http://localhost:8080/mcp"

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

settings = Settings()