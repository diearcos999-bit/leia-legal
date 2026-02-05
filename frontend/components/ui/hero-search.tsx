"use client"

import * as React from "react"
import { useRouter } from "next/navigation"
import { Send, Loader2, Sparkles } from "lucide-react"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

interface HeroSearchProps {
  placeholder?: string
  suggestions?: string[]
  className?: string
}

export function HeroSearch({
  placeholder = "Describe tu situacion legal...",
  suggestions = [],
  className,
}: HeroSearchProps) {
  const [query, setQuery] = React.useState("")
  const [isLoading, setIsLoading] = React.useState(false)
  const [isFocused, setIsFocused] = React.useState(false)
  const router = useRouter()
  const inputRef = React.useRef<HTMLTextAreaElement>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!query.trim() || isLoading) return

    setIsLoading(true)
    router.push(`/chat?q=${encodeURIComponent(query.trim())}`)
  }

  const handleSuggestionClick = (suggestion: string) => {
    setQuery(suggestion)
    inputRef.current?.focus()
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  return (
    <div className={cn("w-full max-w-3xl mx-auto", className)}>
      <form onSubmit={handleSubmit} className="relative">
        {/* Glass container */}
        <div
          className={cn(
            "relative rounded-2xl transition-all duration-500",
            "glass-card",
            isFocused && "shadow-glass-lg glow-pacific"
          )}
        >
          {/* Inner glow effect when focused */}
          <div
            className={cn(
              "absolute inset-0 rounded-2xl transition-opacity duration-500",
              "bg-gradient-to-br from-pacific-400/5 to-transparent",
              isFocused ? "opacity-100" : "opacity-0"
            )}
          />

          {/* Input area */}
          <div className="relative">
            <div className="flex items-center gap-3 px-5 pt-4 pb-2">
              <Sparkles className={cn(
                "h-5 w-5 transition-colors duration-300",
                isFocused ? "text-pacific-500" : "text-slate-400"
              )} />
              <span className={cn(
                "text-xs font-medium transition-colors duration-300",
                isFocused ? "text-pacific-600" : "text-slate-400"
              )}>
                Asistente Legal IA
              </span>
            </div>

            <textarea
              ref={inputRef}
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onFocus={() => setIsFocused(true)}
              onBlur={() => setIsFocused(false)}
              onKeyDown={handleKeyDown}
              placeholder={placeholder}
              rows={2}
              className="w-full resize-none border-0 bg-transparent px-5 py-3 text-lg text-slate-800 placeholder:text-slate-400 focus:outline-none focus:ring-0"
              disabled={isLoading}
            />

            {/* Submit button */}
            <div className="absolute right-3 bottom-3">
              <Button
                type="submit"
                variant="pacific"
                size="lg"
                disabled={!query.trim() || isLoading}
                className="rounded-xl shadow-lg shadow-pacific-500/25"
              >
                {isLoading ? (
                  <Loader2 className="h-5 w-5 animate-spin" />
                ) : (
                  <>
                    <span className="hidden sm:inline mr-2">Enviar</span>
                    <Send className="h-5 w-5" />
                  </>
                )}
              </Button>
            </div>
          </div>
        </div>
      </form>

      {/* Suggestions - subtle pills */}
      {suggestions.length > 0 && (
        <div className="mt-6">
          <p className="text-xs text-slate-400 mb-3 text-center uppercase tracking-wide">O elige una consulta</p>
          <div className="flex flex-wrap gap-2 justify-center">
            {suggestions.map((suggestion, index) => (
              <button
                key={index}
                onClick={() => handleSuggestionClick(suggestion)}
                className="px-4 py-2 text-sm rounded-full text-slate-500 hover:text-slate-800 bg-white/50 hover:bg-white/80 border border-slate-200/50 hover:border-slate-300 transition-all duration-300"
              >
                {suggestion}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
