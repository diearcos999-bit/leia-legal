'use client'

import { type LucideIcon } from 'lucide-react'
import { cn } from '@/lib/utils'

interface StatsCardProps {
  title: string
  value: string | number
  description?: string
  icon?: LucideIcon
  trend?: {
    value: number
    isPositive: boolean
  }
  variant?: 'default' | 'pacific' | 'terracota' | 'success' | 'warning'
}

export function StatsCard({
  title,
  value,
  description,
  icon: Icon,
  trend,
  variant = 'default'
}: StatsCardProps) {
  const variantStyles = {
    default: {
      card: 'glass-card',
      icon: 'bg-slate-100 text-slate-600',
      value: 'text-slate-900'
    },
    pacific: {
      card: 'glass-card border-pacific-200/50',
      icon: 'bg-pacific-100 text-pacific-600',
      value: 'text-pacific-700'
    },
    terracota: {
      card: 'glass-card border-terracota-200/50',
      icon: 'bg-terracota-100 text-terracota-600',
      value: 'text-terracota-700'
    },
    success: {
      card: 'glass-card border-green-200/50',
      icon: 'bg-green-100 text-green-600',
      value: 'text-green-700'
    },
    warning: {
      card: 'glass-card border-amber-200/50',
      icon: 'bg-amber-100 text-amber-600',
      value: 'text-amber-700'
    }
  }

  const styles = variantStyles[variant]

  return (
    <div className={cn('rounded-2xl p-5', styles.card)}>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium text-slate-500">{title}</p>
          <p className={cn('text-2xl font-bold mt-1', styles.value)}>
            {value}
          </p>
          {description && (
            <p className="text-xs text-slate-500 mt-1">{description}</p>
          )}
          {trend && (
            <p className={cn(
              'text-xs font-medium mt-2',
              trend.isPositive ? 'text-green-600' : 'text-red-600'
            )}>
              {trend.isPositive ? '+' : ''}{trend.value}% vs mes anterior
            </p>
          )}
        </div>
        {Icon && (
          <div className={cn('p-3 rounded-xl', styles.icon)}>
            <Icon className="h-5 w-5" />
          </div>
        )}
      </div>
    </div>
  )
}
