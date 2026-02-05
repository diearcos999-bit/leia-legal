'use client'

import { type LucideIcon, FolderOpen } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'

interface EmptyStateProps {
  icon?: LucideIcon
  title: string
  description: string
  action?: {
    label: string
    onClick?: () => void
    href?: string
  }
  className?: string
}

export function EmptyState({
  icon: Icon = FolderOpen,
  title,
  description,
  action,
  className
}: EmptyStateProps) {
  return (
    <div className={cn(
      'glass-card rounded-2xl p-8 lg:p-12 text-center',
      className
    )}>
      <div className="mx-auto w-16 h-16 rounded-2xl bg-slate-100 flex items-center justify-center mb-4">
        <Icon className="h-8 w-8 text-slate-400" />
      </div>
      <h3 className="text-lg font-semibold text-slate-900 mb-2">
        {title}
      </h3>
      <p className="text-sm text-slate-500 max-w-sm mx-auto mb-6">
        {description}
      </p>
      {action && (
        action.href ? (
          <Button variant="pacific" asChild>
            <a href={action.href}>{action.label}</a>
          </Button>
        ) : (
          <Button variant="pacific" onClick={action.onClick}>
            {action.label}
          </Button>
        )
      )}
    </div>
  )
}
