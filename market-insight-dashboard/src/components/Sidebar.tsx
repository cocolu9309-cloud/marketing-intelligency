'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { clsx } from 'clsx'
import {
  Target,
  TrendingUp,
  Building2,
  Search,
  FileText,
  Settings,
} from 'lucide-react'

const navItems = [
  { href: '/', label: '机会列表', icon: Target },
  { href: '/trends', label: '趋势监控', icon: TrendingUp },
  { href: '/competitors', label: '竞品档案', icon: Building2 },
  { href: '/search', label: '搜索洞察', icon: Search },
  { href: '/briefs', label: 'Brief管理', icon: FileText },
  { href: '/settings', label: '设置', icon: Settings },
]

export default function Sidebar() {
  const pathname = usePathname()

  return (
    <aside className="fixed left-0 top-0 h-screen w-64 bg-slate-900 text-white">
      <div className="p-6">
        <h1 className="text-xl font-bold flex items-center gap-2">
          <span>🔥</span>
          市场洞察工作台
        </h1>
      </div>
      <nav className="mt-6">
        {navItems.map((item) => {
          const Icon = item.icon
          const isActive = pathname === item.href
          return (
            <Link
              key={item.href}
              href={item.href}
              className={clsx(
                'flex items-center gap-3 px-6 py-3 text-sm transition-colors',
                isActive
                  ? 'bg-slate-800 text-white border-l-2 border-primary-500'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800'
              )}
            >
              <Icon size={18} />
              {item.label}
            </Link>
          )
        })}
      </nav>
    </aside>
  )
}