'use client'

import { useState, useEffect } from 'react'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

interface Competitor {
  id: string
  brand: string
  url: string
  category: string
  has_custom_product: string
  marketing_email: string
  notes: string
  created_at: string
}

export default function CompetitorsPage() {
  const [competitors, setCompetitors] = useState<Competitor[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('')

  useEffect(() => {
    fetch(`${API_BASE}/competitors/`).then(res => res.json()).then(data => {
      setCompetitors(data)
      setLoading(false)
    }).catch(() => setLoading(false))
  }, [])

  const filtered = competitors.filter(c =>
    c.brand?.includes(filter) ||
    c.category?.includes(filter) ||
    c.url?.includes(filter)
  )

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">竞品档案</h2>

      <div className="mb-4">
        <input
          type="text"
          placeholder="搜索品牌、品类或网址..."
          value={filter}
          onChange={e => setFilter(e.target.value)}
          className="w-full max-w-md px-4 py-2 border rounded-lg"
        />
      </div>

      <div className="text-sm text-slate-500 mb-4">共 {filtered.length} 个竞品</div>

      {loading ? (
        <div className="text-center py-12 text-slate-500">加载中...</div>
      ) : filtered.length === 0 ? (
        <div className="text-center py-12 text-slate-500">暂无竞品数据</div>
      ) : (
        <div className="space-y-4">
          {filtered.map((comp: Competitor) => (
            <div key={comp.id} className="border rounded-lg p-4 bg-white">
              <div className="flex items-start justify-between mb-2">
                <div>
                  <a href={comp.url} target="_blank" rel="noopener noreferrer" className="font-medium text-primary-600 hover:underline">
                    {comp.brand || comp.url}
                  </a>
                  {comp.brand && comp.url && (
                    <span className="text-slate-400 ml-2 text-sm">({new URL(comp.url).hostname})</span>
                  )}
                </div>
                <span className={`text-xs px-2 py-1 rounded ${comp.has_custom_product === '完全定制' ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700'}`}>
                  {comp.has_custom_product}
                </span>
              </div>
              <div className="text-sm text-slate-600 mb-2">{comp.category}</div>
              {comp.marketing_email && (
                <div className="text-sm text-slate-500">📧 {comp.marketing_email}</div>
              )}
              {comp.notes && (
                <div className="text-sm text-slate-400 mt-1">📝 {comp.notes}</div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}