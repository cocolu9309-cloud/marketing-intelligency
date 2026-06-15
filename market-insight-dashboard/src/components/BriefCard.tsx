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
