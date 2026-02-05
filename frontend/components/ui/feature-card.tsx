"use client"

import * as React from "react"
import { LucideIcon } from "lucide-react"
import { cn } from "@/lib/utils"

interface FeatureCardProps {
  icon: LucideIcon
  title: string
  description: string
  features?: string[]
  className?: string
  iconClassName?: string
}

export function FeatureCard({
  icon: Icon,
  title,
  description,
  features,
  className,
  iconClassName,
}: FeatureCardProps) {
  return (
    <div
      className={cn(
        "group relative p-6 rounded-2xl bg-white border border-pacific-100/50",
        "shadow-sm hover:shadow-premium transition-all duration-300",
        "hover:border-pacific-200/50 hover:-translate-y-1",
        className
      )}
    >
      {/* Icon Container */}
      <div
        className={cn(
          "inline-flex items-center justify-center",
          "h-14 w-14 rounded-xl mb-5",
          "bg-gradient-to-br from-pacific-50 to-pacific-100/50",
          "group-hover:from-terracota-50 group-hover:to-terracota-100/50",
          "transition-colors duration-300",
          iconClassName
        )}
      >
        <Icon className="h-7 w-7 text-pacific-700 group-hover:text-terracota-600 transition-colors" />
      </div>

      {/* Content */}
      <h3 className="text-lg font-semibold text-slate-900 mb-2">
        {title}
      </h3>
      <p className="text-muted-foreground text-sm mb-4">
        {description}
      </p>

      {/* Feature List */}
      {features && features.length > 0 && (
        <ul className="space-y-2">
          {features.map((feature, index) => (
            <li
              key={index}
              className="flex items-start gap-2 text-sm text-slate-700"
            >
              <span className="h-1.5 w-1.5 rounded-full bg-terracota-400 mt-1.5 flex-shrink-0" />
              {feature}
            </li>
          ))}
        </ul>
      )}

      {/* Hover Accent */}
      <div className="absolute bottom-0 left-6 right-6 h-0.5 bg-gradient-to-r from-pacific-400 to-pacific-300 opacity-0 group-hover:opacity-100 transition-opacity rounded-full" />
    </div>
  )
}
