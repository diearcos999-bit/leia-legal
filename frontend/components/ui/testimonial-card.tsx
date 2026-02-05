"use client"

import * as React from "react"
import { Star } from "lucide-react"
import { cn } from "@/lib/utils"

interface TestimonialCardProps {
  quote: string
  author: string
  role: string
  rating?: number
  avatarInitials?: string
  featured?: boolean
  className?: string
}

export function TestimonialCard({
  quote,
  author,
  role,
  rating = 5,
  avatarInitials,
  featured = false,
  className,
}: TestimonialCardProps) {
  const initials = avatarInitials || author.split(" ").map(n => n[0]).join("").slice(0, 2)

  return (
    <div
      className={cn(
        "relative p-6 rounded-2xl transition-all duration-300",
        featured
          ? "bg-gradient-to-br from-navy-900 to-navy-800 text-white shadow-navy"
          : "bg-white border border-navy-100/50 shadow-sm hover:shadow-premium hover:-translate-y-1",
        className
      )}
    >
      {/* Rating Stars */}
      <div className="flex gap-1 mb-4">
        {Array.from({ length: 5 }).map((_, i) => (
          <Star
            key={i}
            className={cn(
              "h-4 w-4",
              i < rating
                ? featured
                  ? "fill-gold-400 text-gold-400"
                  : "fill-gold-400 text-gold-400"
                : featured
                  ? "fill-navy-700 text-navy-700"
                  : "fill-navy-100 text-navy-100"
            )}
          />
        ))}
      </div>

      {/* Quote */}
      <blockquote
        className={cn(
          "text-base mb-6 leading-relaxed",
          featured ? "text-white/90" : "text-navy-700"
        )}
      >
        &ldquo;{quote}&rdquo;
      </blockquote>

      {/* Author */}
      <div className="flex items-center gap-3">
        {/* Avatar */}
        <div
          className={cn(
            "h-10 w-10 rounded-full flex items-center justify-center text-sm font-semibold",
            featured
              ? "bg-gold-400 text-navy-900"
              : "bg-gradient-to-br from-navy-100 to-navy-200 text-navy-700"
          )}
        >
          {initials}
        </div>

        <div>
          <p
            className={cn(
              "font-semibold text-sm",
              featured ? "text-white" : "text-navy-900"
            )}
          >
            {author}
          </p>
          <p
            className={cn(
              "text-xs",
              featured ? "text-white/70" : "text-muted-foreground"
            )}
          >
            {role}
          </p>
        </div>
      </div>

      {/* Decorative quote mark for featured */}
      {featured && (
        <div className="absolute top-4 right-4 text-6xl text-navy-700/30 font-serif leading-none">
          &rdquo;
        </div>
      )}
    </div>
  )
}
