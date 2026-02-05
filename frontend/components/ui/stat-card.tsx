"use client"

import * as React from "react"
import { cn } from "@/lib/utils"

interface StatCardProps {
  value: string
  label: string
  suffix?: string
  className?: string
}

export function StatCard({ value, label, suffix, className }: StatCardProps) {
  const [isVisible, setIsVisible] = React.useState(false)
  const [displayValue, setDisplayValue] = React.useState("0")
  const ref = React.useRef<HTMLDivElement>(null)

  React.useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true)
        }
      },
      { threshold: 0.1 }
    )

    if (ref.current) {
      observer.observe(ref.current)
    }

    return () => observer.disconnect()
  }, [])

  React.useEffect(() => {
    if (!isVisible) return

    // Extract numeric value
    const numericValue = parseInt(value.replace(/\D/g, ""), 10)
    if (isNaN(numericValue)) {
      setDisplayValue(value)
      return
    }

    // Animate counter
    const duration = 2000
    const steps = 60
    const stepDuration = duration / steps
    const increment = numericValue / steps

    let current = 0
    let step = 0

    const timer = setInterval(() => {
      step++
      current = Math.min(Math.round(increment * step), numericValue)

      // Format with the same prefix (like "+") if present
      const prefix = value.match(/^[^\d]*/)?.[0] || ""
      setDisplayValue(prefix + current.toLocaleString())

      if (step >= steps) {
        clearInterval(timer)
        setDisplayValue(value) // Ensure final value is exact
      }
    }, stepDuration)

    return () => clearInterval(timer)
  }, [isVisible, value])

  return (
    <div
      ref={ref}
      className={cn(
        "text-center p-4 transition-all duration-500",
        isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4",
        className
      )}
    >
      <div className="flex items-baseline justify-center gap-1">
        <span className="text-3xl lg:text-4xl font-bold text-slate-900 tabular-nums">
          {displayValue}
        </span>
        {suffix && (
          <span className="text-lg text-pacific-500 font-semibold">{suffix}</span>
        )}
      </div>
      <p className="text-sm text-muted-foreground mt-1">{label}</p>
    </div>
  )
}

interface StatGridProps {
  stats: Array<{
    value: string
    label: string
    suffix?: string
  }>
  className?: string
}

export function StatGrid({ stats, className }: StatGridProps) {
  return (
    <div
      className={cn(
        "grid grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-8",
        className
      )}
    >
      {stats.map((stat, index) => (
        <StatCard
          key={index}
          value={stat.value}
          label={stat.label}
          suffix={stat.suffix}
        />
      ))}
    </div>
  )
}
