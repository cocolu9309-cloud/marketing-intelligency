'use client'

import { useState, useEffect } from 'react'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

export default function SearchPage() {
  const [opportunities, setOpportunities] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`${API_BASE}/search/`).then(res => res.json()).then(data => {
      setOpportunities(data)
      setLoading(false)
    }).catch(() => setLoading(false))
  }, [])

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">搜索洞察</h2>
      {loading ? (
        <div className="text-center py-12 text-slate-500">加载中...</div>
      ) : opportunities.length === 0 ? (
        <div className="text-center py-12 text-slate-500">暂无搜索数据</div>
      ) : (
        <div className="bg-white border rounded-lg overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-slate-50">
              <tr>
                <th className="text-left p-3">关键词</th>
                <th className="text-left p-3">搜索意图</th>
                <th className="text-left p-3">推荐页面</th>
                <th className="text-right p-3">优先级</th>
              </tr>
            </thead>
            <tbody>
              {opportunities.map((item: any) => (
                <tr key={item.id} className="border-t">
                  <td className="p-3 font-medium">{item.keyword}</td>
                  <td className="p-3 text-slate-600">{item.search_intent}</td>
                  <td className="p-3 text-slate-600">{item.recommended_page_type}</td>
                  <td className="p-3 text-right">
                    <span className={`px-2 py-1 rounded text-xs ${
                      item.priority >= 4 ? 'bg-green-100 text-green-700' :
                      item.priority >= 3 ? 'bg-yellow-100 text-yellow-700' :
                      'bg-gray-100 text-gray-600'
                    }`}>
                      {item.priority}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
