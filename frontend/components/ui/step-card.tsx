import * as React from "react"
import { LucideIcon } from "lucide-react"
import { cn } from "@/lib/utils"

interface StepCardProps {
  number: number
  icon: LucideIcon
  title: string
  description: string
  className?: string
}

export function StepCard({
  number,
  icon: Icon,
  title,
  description,
  className,
}: StepCardProps) {
  return (
    <div
      className={cn(
        "relative flex flex-col items-center text-center p-6",
        className
      )}
    >
      {/* Step number badge */}
      <div className="absolute -top-3 left-1/2 -translate-x-1/2">
        <span className="inline-flex items-center justify-center w-6 h-6 text-xs font-bold text-white bg-pacific-600 rounded-full">
          {number}
        </span>
      </div>

      {/* Icon container */}
      <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-pacific-100 to-pacific-50 flex items-center justify-center mb-4 shadow-sm">
        <Icon className="w-8 h-8 text-pacific-600" />
      </div>

      {/* Content */}
      <h3 className="font-semibold text-slate-900 mb-2">{title}</h3>
      <p className="text-sm text-slate-600">{description}</p>
    </div>
  )
}

// Horizontal stepper with connectors
interface StepperProps {
  children: React.ReactNode
  className?: string
}

export function Stepper({ children, className }: StepperProps) {
  const childrenArray = React.Children.toArray(children)

  return (
    <div className={cn("relative", className)}>
      {/* Connector line - hidden on mobile */}
      <div className="hidden md:block absolute top-8 left-[15%] right-[15%] h-0.5 bg-gradient-to-r from-pacific-200 via-pacific-300 to-pacific-200" />

      {/* Steps */}
      <div className="grid md:grid-cols-3 gap-8 relative">
        {childrenArray.map((child, index) => (
          <div key={index} className="relative">
            {/* Connector dots on mobile */}
            {index < childrenArray.length - 1 && (
              <div className="md:hidden absolute -bottom-4 left-1/2 -translate-x-1/2 flex gap-1">
                <div className="w-1.5 h-1.5 rounded-full bg-pacific-300" />
                <div className="w-1.5 h-1.5 rounded-full bg-pacific-300" />
                <div className="w-1.5 h-1.5 rounded-full bg-pacific-300" />
              </div>
            )}
            {child}
          </div>
        ))}
      </div>
    </div>
  )
}
