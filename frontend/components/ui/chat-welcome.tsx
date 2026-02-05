'use client'

import { LeiaAvatar } from './leia-avatar'
import { Sparkles, Scale, ArrowRight } from 'lucide-react'
import { cn } from '@/lib/utils'

interface ChatWelcomeProps {
  className?: string
  onSuggestionClick?: (suggestion: string) => void
}

const suggestions = [
  { text: "Me despidieron sin aviso", icon: "briefcase" },
  { text: "Pension alimenticia", icon: "heart" },
  { text: "Deudas que no puedo pagar", icon: "credit-card" },
  { text: "Problemas con mi arriendo", icon: "home" },
]

export function ChatWelcome({ className, onSuggestionClick }: ChatWelcomeProps) {
  return (
    <div className={cn("flex flex-col items-center text-center py-8 px-4", className)}>
      {/* Avatar animado */}
      <div className="mb-6 animate-fade-in-up">
        <LeiaAvatar size="xl" animated />
      </div>

      {/* Saludo principal */}
      <div className="animate-fade-in-up" style={{ animationDelay: '150ms' }}>
        <h1 className="text-3xl sm:text-4xl font-semibold text-slate-900 mb-3">
          Hola, soy <span className="text-gradient">LEIA</span>
        </h1>
        <p className="text-lg text-slate-600 mb-2">
          Tu asistente legal con inteligencia artificial
        </p>
      </div>

      {/* Descripcion */}
      <div className="animate-fade-in-up max-w-lg" style={{ animationDelay: '300ms' }}>
        <p className="text-slate-500 mb-6">
          Cuentame tu situacion legal y te ayudare a entender tus derechos.
          Si necesitas asistencia profesional, te conectare con el abogado adecuado para tu caso.
        </p>
      </div>

      {/* Badges de confianza */}
      <div className="flex flex-wrap justify-center gap-3 mb-8 animate-fade-in-up" style={{ animationDelay: '450ms' }}>
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full glass-button text-sm">
          <Sparkles className="h-4 w-4 text-pacific-500" />
          <span className="text-slate-600">Respuestas inmediatas</span>
        </div>
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full glass-button text-sm">
          <Scale className="h-4 w-4 text-pacific-500" />
          <span className="text-slate-600">Abogados verificados</span>
        </div>
      </div>

      {/* Sugerencias rapidas */}
      <div className="w-full max-w-md animate-fade-in-up" style={{ animationDelay: '600ms' }}>
        <p className="text-sm text-slate-500 mb-3">Consultas frecuentes:</p>
        <div className="grid grid-cols-2 gap-2">
          {suggestions.map((suggestion, index) => (
            <button
              key={index}
              onClick={() => onSuggestionClick?.(suggestion.text)}
              className={cn(
                "group flex items-center justify-between gap-2 p-3 rounded-xl text-left transition-all duration-200",
                "glass-card-hover text-sm text-slate-700 hover:text-slate-900"
              )}
            >
              <span>{suggestion.text}</span>
              <ArrowRight className="h-4 w-4 opacity-0 -translate-x-2 group-hover:opacity-100 group-hover:translate-x-0 transition-all text-pacific-500" />
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
