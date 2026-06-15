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
