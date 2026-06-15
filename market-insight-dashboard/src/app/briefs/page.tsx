'use client'

import { useState, useEffect } from 'react'
import BriefCard from '@/components/BriefCard'
import { Brief } from '@/types'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

export default function BriefsPage() {
  const [briefs, setBriefs] = useState<Brief[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchBriefs()
  }, [])

  const fetchBriefs = async () => {
    setLoading(true)
    try {
      const res = await fetch(`${API_BASE}/briefs/`)
      const data = await res.json()
      setBriefs(data)
    } catch (error) {
      console.error('Failed to fetch briefs:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleStatusChange = async (briefId: string, newStatus: string) => {
    try {
      await fetch(`${API_BASE}/briefs/${briefId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus }),
      })
      fetchBriefs()
    } catch (error) {
      console.error('Failed to update brief status:', error)
    }
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold">Brief 管理</h2>
        <span className="text-sm text-slate-500">共 {briefs.length} 条</span>
      </div>

      {loading ? (
        <div className="text-center py-12 text-slate-500">加载中...</div>
      ) : briefs.length === 0 ? (
        <div className="text-center py-12 text-slate-500">
          暂无 Brief 数据
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {briefs.map((brief) => (
            <BriefCard key={brief.id} brief={brief} onStatusChange={handleStatusChange} />
          ))}
        </div>
      )}
    </div>
  )
}
