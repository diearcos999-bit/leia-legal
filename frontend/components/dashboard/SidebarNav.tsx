'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { cn } from '@/lib/utils'
import { useRole } from '@/lib/hooks/useRole'

export function SidebarNav() {
  const pathname = usePathname()
  const { navigation } = useRole()

  return (
    <div className="space-y-1">
      <p className="px-3 mb-2 text-xs font-semibold text-slate-500 uppercase tracking-wider">
        Menu
      </p>
      {navigation.map((item) => {
        const Icon = item.icon
        const isActive = pathname === item.href || pathname.startsWith(item.href + '/')

        return (
          <Link
            key={item.href}
            href={item.href}
            className={cn(
              'flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-200',
              isActive
                ? 'bg-pacific-500/10 text-pacific-700 shadow-sm'
                : 'text-slate-600 hover:text-slate-900 hover:bg-white/50'
            )}
          >
            <Icon className={cn(
              'h-5 w-5 flex-shrink-0',
              isActive ? 'text-pacific-600' : 'text-slate-400'
            )} />
            <span className="truncate">{item.label}</span>
            {item.badge && (
              <span className={cn(
                'ml-auto px-2 py-0.5 text-xs font-medium rounded-full',
                isActive
                  ? 'bg-pacific-500 text-white'
                  : 'bg-slate-200 text-slate-600'
              )}>
                {item.badge}
              </span>
            )}
          </Link>
        )
      })}
    </div>
  )
}
