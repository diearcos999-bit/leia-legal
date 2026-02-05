"use client"

import * as React from "react"
import Link from "next/link"
import { LucideIcon } from "lucide-react"
import { cn } from "@/lib/utils"

interface AreaCardProps {
  name: string
  icon: LucideIcon
  href: string
  color?: "pacific" | "terracota"
  description?: string
  className?: string
}

export function AreaCard({
  name,
  icon: Icon,
  href,
  color = "pacific",
  description,
  className,
}: AreaCardProps) {
  const colorStyles = {
    pacific: {
      bg: "bg-pacific-50 hover:bg-pacific-100",
      border: "border-pacific-100 hover:border-pacific-200",
      icon: "text-pacific-600",
      text: "text-pacific-900",
      description: "text-pacific-600",
    },
    terracota: {
      bg: "bg-terracota-50 hover:bg-terracota-100",
      border: "border-terracota-100 hover:border-terracota-200",
      icon: "text-terracota-600",
      text: "text-terracota-900",
      description: "text-terracota-600",
    },
  }

  const styles = colorStyles[color]

  return (
    <Link
      href={href}
      className={cn(
        "group flex flex-col items-center p-6 rounded-xl border transition-all duration-200",
        "hover:shadow-md hover:-translate-y-0.5",
        styles.bg,
        styles.border,
        className
      )}
    >
      <div
        className={cn(
          "w-12 h-12 rounded-xl flex items-center justify-center mb-3 transition-transform group-hover:scale-110",
          color === "pacific" ? "bg-pacific-100" : "bg-terracota-100"
        )}
      >
        <Icon className={cn("w-6 h-6", styles.icon)} />
      </div>
      <span className={cn("font-semibold text-sm", styles.text)}>{name}</span>
      {description && (
        <span className={cn("text-xs mt-1 text-center", styles.description)}>
          {description}
        </span>
      )}
    </Link>
  )
}

// Grid component for area cards
interface AreaGridProps {
  children: React.ReactNode
  className?: string
}

export function AreaGrid({ children, className }: AreaGridProps) {
  return (
    <div
      className={cn(
        "grid grid-cols-2 md:grid-cols-4 gap-4",
        className
      )}
    >
      {children}
    </div>
  )
}
