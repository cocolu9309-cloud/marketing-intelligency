'use client'

import { DEPARTMENTS, STATUS_OPTIONS, GRADE_OPTIONS } from '@/types'

interface FilterBarProps {
  filters: {
    department: string
    status: string
    grade: string
  }
  onFilterChange: (key: string, value: string) => void
}

export default function FilterBar({ filters, onFilterChange }: FilterBarProps) {
  return (
    <div className="flex gap-4 mb-6">
      <select
        value={filters.department}
        onChange={(e) => onFilterChange('department', e.target.value)}
        className="px-4 py-2 border rounded-lg text-sm"
      >
        <option value="">部门（全部）</option>
        {DEPARTMENTS.map((d) => (
          <option key={d} value={d}>{d}</option>
        ))}
      </select>
      <select
        value={filters.status}
        onChange={(e) => onFilterChange('status', e.target.value)}
        className="px-4 py-2 border rounded-lg text-sm"
      >
        <option value="">状态（全部）</option>
        {STATUS_OPTIONS.map((s) => (
          <option key={s} value={s}>{s}</option>
        ))}
      </select>
      <select
        value={filters.grade}
        onChange={(e) => onFilterChange('grade', e.target.value)}
        className="px-4 py-2 border rounded-lg text-sm"
      >
        <option value="">等级（全部）</option>
        {GRADE_OPTIONS.map((g) => (
          <option key={g} value={g}>{g}级</option>
        ))}
      </select>
    </div>
  )
}