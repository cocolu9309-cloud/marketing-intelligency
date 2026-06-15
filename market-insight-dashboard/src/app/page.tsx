'use client'

import { useState, useEffect } from 'react'
import FilterBar from '@/components/FilterBar'
import OpportunityCard from '@/components/OpportunityCard'
import { Opportunity } from '@/types'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

export default function OpportunitiesPage() {
  const [opportunities, setOpportunities] = useState<Opportunity[]>([])
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState({
    department: '',
    status: '',
    grade: '',
  })

  useEffect(() => {
    fetchOpportunities()
  }, [filters])

  const fetchOpportunities = async () => {
    setLoading(true)
    try {
      const params = new URLSearchParams()
      if (filters.department) params.append('department', filters.department)
      if (filters.status) params.append('status', filters.status)
      if (filters.grade) params.append('grade', filters.grade)

      const res = await fetch(`${API_BASE}/opportunities/?${params}`)
      const data = await res.json()
      setOpportunities(data)
    } catch (error) {
      console.error('Failed to fetch opportunities:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleFilterChange = (key: string, value: string) => {
    setFilters((prev) => ({ ...prev, [key]: value }))
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold">机会列表</h2>
        <span className="text-sm text-slate-500">共 {opportunities.length} 条</span>
      </div>

      <FilterBar filters={filters} onFilterChange={handleFilterChange} />

      {loading ? (
        <div className="text-center py-12 text-slate-500">加载中...</div>
      ) : opportunities.length === 0 ? (
        <div className="text-center py-12 text-slate-500">
          暂无机会数据
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {opportunities.map((opp) => (
            <OpportunityCard key={opp.id} opportunity={opp} />
          ))}
        </div>
      )}
    </div>
  )
}