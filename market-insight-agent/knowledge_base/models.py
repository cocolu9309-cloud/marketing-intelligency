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