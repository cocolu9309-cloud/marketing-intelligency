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
