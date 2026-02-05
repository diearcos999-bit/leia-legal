'use client'

import { type LucideIcon } from 'lucide-react'
import { cn } from '@/lib/utils'

interface PageHeaderProps {
  title: string
  description?: string
  icon?: LucideIcon
  action?: React.ReactNode
  className?: string
}

export function PageHeader({
  title,
  description,
  icon: Icon,
  action,
  className
}: PageHeaderProps) {
  return (
    <div className={cn('mb-6 lg:mb-8', className)}>
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div className="flex items-center gap-3">
          {Icon && (
            <div className="p-2.5 rounded-xl bg-pacific-100">
              <Icon className="h-6 w-6 text-pacific-600" />
            </div>
          )}
          <div>
            <h1 className="text-2xl lg:text-3xl font-bold text-slate-900">{title}</h1>
            {description && (
              <p className="text-sm text-slate-500 mt-0.5">{description}</p>
            )}
          </div>
        </div>
        {action && (
          <div className="flex-shrink-0">
            {action}
          </div>
        )}
      </div>
    </div>
  )
}
