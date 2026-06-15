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

interface CompetitorAction {
  id: string
  competitor: string
  action_type: string
  description: string
  possible_goal: string
  should_follow: boolean
  suggested_action: string
  created_at: string
}

export default function CompetitorsPage() {
  const [competitors, setCompetitors] = useState<Competitor[]>([])
  const [actions, setActions] = useState<CompetitorAction[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('')
  const [activeTab, setActiveTab] = useState<'list' | 'actions'>('list')

  useEffect(() => {
    Promise.all([
      fetch(`${API_BASE}/competitors/`).then(res => res.json()),
      fetch(`${API_BASE}/competitors/actions/`).then(res => res.json())
    ]).then(([compData, actionData]) => {
      setCompetitors(compData)
      setActions(actionData)
      setLoading(false)
    }).catch(() => setLoading(false))
  }, [])

  const filteredCompetitors = competitors.filter(c =>
    c.brand?.includes(filter) ||
    c.category?.includes(filter) ||
    c.url?.includes(filter)
  )

  const filteredActions = actions.filter(a =>
    a.competitor?.includes(filter) ||
    a.description?.includes(filter)
  )

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">竞品档案</h2>

      {/* Tab切换 */}
      <div className="flex gap-4 mb-6 border-b">
        <button
          onClick={() => setActiveTab('list')}
          className={`pb-2 px-1 text-sm font-medium ${activeTab === 'list' ? 'border-b-2 border-primary-500 text-primary-600' : 'text-slate-500'}`}
        >
          竞品清单 ({competitors.length})
        </button>
        <button
          onClick={() => setActiveTab('actions')}
          className={`pb-2 px-1 text-sm font-medium ${activeTab === 'actions' ? 'border-b-2 border-primary-500 text-primary-600' : 'text-slate-500'}`}
        >
          竞品动态 ({actions.length})
        </button>
      </div>

      <div className="mb-4">
        <input
          type="text"
          placeholder={activeTab === 'list' ? "搜索品牌、品类或网址..." : "搜索竞品或动态描述..."}
          value={filter}
          onChange={e => setFilter(e.target.value)}
          className="w-full max-w-md px-4 py-2 border rounded-lg"
        />
      </div>

      {loading ? (
        <div className="text-center py-12 text-slate-500">加载中...</div>
      ) : activeTab === 'list' ? (
        <>
          <div className="text-sm text-slate-500 mb-4">共 {filteredCompetitors.length} 个竞品</div>
          {filteredCompetitors.length === 0 ? (
            <div className="text-center py-12 text-slate-500">暂无竞品数据</div>
          ) : (
            <div className="space-y-4">
              {filteredCompetitors.map((comp: Competitor) => (
                <div key={comp.id} className="border rounded-lg p-4 bg-white">
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <a href={comp.url} target="_blank" rel="noopener noreferrer" className="font-medium text-primary-600 hover:underline">
                        {comp.brand || new URL(comp.url).hostname}
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
        </>
      ) : (
        <>
          <div className="text-sm text-slate-500 mb-4">共 {filteredActions.length} 条动态</div>
          {filteredActions.length === 0 ? (
            <div className="text-center py-12 text-slate-500">暂无竞品动态</div>
          ) : (
            <div className="space-y-4">
              {filteredActions.map((action: CompetitorAction) => (
                <div key={action.id} className="border rounded-lg p-4 bg-white">
                  <div className="flex items-start justify-between mb-2">
                    <span className="font-medium text-slate-800">{action.competitor}</span>
                    <div className="flex items-center gap-2">
                      <span className={`text-xs px-2 py-1 rounded ${action.should_follow ? 'bg-red-100 text-red-700' : 'bg-slate-100 text-slate-600'}`}>
                        {action.action_type}
                      </span>
                      {action.should_follow && (
                        <span className="text-xs px-2 py-1 bg-blue-100 text-blue-700 rounded">值得跟进</span>
                      )}
                    </div>
                  </div>
                  <p className="text-sm text-slate-600 mb-2">{action.description}</p>
                  {action.suggested_action && (
                    <p className="text-sm text-primary-600">💡 {action.suggested_action}</p>
                  )}
                  <div className="text-xs text-slate-400 mt-2">
                    {new Date(action.created_at).toLocaleDateString('zh-CN')}
                  </div>
                </div>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  )
}