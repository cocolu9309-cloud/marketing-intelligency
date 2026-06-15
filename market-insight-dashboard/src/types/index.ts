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