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