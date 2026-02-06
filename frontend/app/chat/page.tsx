'use client'

import { useState, useRef, useEffect, Suspense } from 'react'
import { useSearchParams } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { LeiaAvatar } from '@/components/ui/leia-avatar'
import { Send, User, ArrowLeft, Sparkles, ThumbsUp, ThumbsDown, Loader2, Scale, ChevronRight, LogIn } from 'lucide-react'
import { LeiaLogo } from '@/components/ui/leia-logo'
import Link from 'next/link'
import { cn } from '@/lib/utils'
import { LawyerModal } from '@/components/lawyer-modal'
import { AuthModal } from '@/components/auth-modal'
import { useAuth } from '@/hooks/useAuth'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
  feedback?: 'helpful' | 'not_helpful' | null
  correction?: string
  showLawyerButton?: boolean
  suggestedSpecialties?: string[]
}

interface Lawyer {
  id: number
  name: string
  specialty: string
  rating: number
  reviews_count: number
  location: string
  price_display: string
  is_verified: boolean
  match_score?: number
  experience?: string
}

interface ReferralSuggestion {
  should_refer: boolean
  urgency: string
  reason: string
  specialties: string[]
}

// Suggestions for pre-chat screen
const suggestions = [
  "Me despidieron sin aviso",
  "Pension alimenticia",
  "Deudas que no puedo pagar",
  "Problemas con mi arriendo",
]

function ChatContent() {
  const searchParams = useSearchParams()
  const initialQuery = searchParams.get('q')
  const initialArea = searchParams.get('area')

  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [showCorrectionFor, setShowCorrectionFor] = useState<string | null>(null)
  const [correctionText, setCorrectionText] = useState('')
  const [isFocused, setIsFocused] = useState(false)
  const [chatStarted, setChatStarted] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const initialQueryProcessed = useRef(false)

  // Modal state
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [modalLawyers, setModalLawyers] = useState<Lawyer[]>([])
  const [modalLegalArea, setModalLegalArea] = useState('')
  const [loadingLawyers, setLoadingLawyers] = useState(false)

  // Auth state
  const {
    isAuthenticated,
    isLoading: authLoading,
    canAskQuestion,
    remainingQuestions,
    user,
    login,
    register,
    logout,
    incrementQuestionCount,
    QUESTION_LIMIT
  } = useAuth()
  const [showAuthModal, setShowAuthModal] = useState(false)
  const [authModalReason, setAuthModalReason] = useState<'limit' | 'lawyer'>('limit')

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    if ((initialQuery || initialArea) && !initialQueryProcessed.current) {
      initialQueryProcessed.current = true
      setChatStarted(true)
      if (initialQuery) {
        setTimeout(() => {
          handleSubmitMessage(initialQuery)
        }, 300)
      }
    }
  }, [initialQuery, initialArea])

  const handleFeedback = async (messageId: string, feedback: 'helpful' | 'not_helpful') => {
    setMessages(prev => prev.map(msg =>
      msg.id === messageId ? { ...msg, feedback } : msg
    ))
    if (feedback === 'not_helpful') {
      setShowCorrectionFor(messageId)
    } else {
      setShowCorrectionFor(null)
      await saveFeedback(messageId, feedback, null)
    }
  }

  const handleCorrectionSubmit = async (messageId: string) => {
    if (!correctionText.trim()) return
    setMessages(prev => prev.map(msg =>
      msg.id === messageId ? { ...msg, correction: correctionText } : msg
    ))
    await saveFeedback(messageId, 'not_helpful', correctionText)
    setCorrectionText('')
    setShowCorrectionFor(null)
  }

  const saveFeedback = async (messageId: string, feedback: string, correction: string | null) => {
    try {
      const message = messages.find(m => m.id === messageId)
      const previousMessage = messages[messages.indexOf(message!) - 1]
      await fetch(`${API_URL}/api/feedback`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message_id: messageId,
          user_question: previousMessage?.content || '',
          ai_response: message?.content || '',
          feedback,
          correction,
          timestamp: new Date().toISOString()
        })
      })
    } catch (error) {
      console.error('Error saving feedback:', error)
    }
  }

  // Open modal and fetch lawyers - NO requiere auth para VER abogados
  const handleOpenLawyerModal = async (specialties: string[]) => {
    setLoadingLawyers(true)
    // Ensure we have a valid specialty, default to Derecho Civil if empty
    const legalArea = (specialties && specialties.length > 0 && specialties[0]) ? specialties[0] : 'Derecho Civil'
    setModalLegalArea(legalArea)

    try {
      const response = await fetch(`${API_URL}/api/lawyers/match`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          legal_area: legalArea.replace('Derecho ', ''),
          region: 'Santiago'
        })
      })

      if (response.ok) {
        const data = await response.json()
        setModalLawyers(data.lawyers || [])
      }
    } catch (error) {
      console.error('Error fetching lawyers:', error)
    } finally {
      setLoadingLawyers(false)
      setIsModalOpen(true)
    }
  }

  const handleTransferComplete = (lawyerId: number) => {
    // Add a system message about the transfer
    const transferMessage: Message = {
      id: Date.now().toString(),
      role: 'assistant',
      content: `✅ Tu caso ha sido enviado al abogado. Te contactaran pronto.\n\nMientras esperas, puedo seguir ayudandote con otras consultas.`,
      timestamp: new Date()
    }
    setMessages(prev => [...prev, transferMessage])
  }

  const handleSubmitMessage = async (messageText: string) => {
    if (!messageText.trim() || isLoading) return

    // Check if user can ask questions (unregistered users have a limit)
    if (!isAuthenticated && !canAskQuestion) {
      setAuthModalReason('limit')
      setShowAuthModal(true)
      return
    }

    // Si es el primer mensaje, marcar que el chat ha comenzado
    if (!chatStarted) {
      setChatStarted(true)
    }

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: messageText,
      timestamp: new Date()
    }

    // El mensaje del usuario aparece primero
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      // Use the new v2 chat endpoint with triage
      const response = await fetch(`${API_URL}/api/v2/chat/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: messageText,
          conversation_history: messages.map(m => ({
            role: m.role,
            content: m.content
          }))
        }),
      })

      if (!response.ok) throw new Error('Error en la respuesta')

      const data = await response.json()

      // Check if we should show lawyer button
      const referral: ReferralSuggestion | null = data.referral

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.response,
        timestamp: new Date(),
        showLawyerButton: referral?.should_refer || false,
        suggestedSpecialties: referral?.specialties || []
      }

      setMessages(prev => [...prev, assistantMessage])

      // Increment question count for unregistered users
      if (!isAuthenticated) {
        incrementQuestionCount()
      }
    } catch (error) {
      console.error('Error:', error)
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `Lo siento, hubo un error al procesar tu consulta. Por favor intenta nuevamente.\n\nSi el problema persiste, verifica que el backend este corriendo en ${API_URL}`,
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    await handleSubmitMessage(input)
  }

  const handleSuggestionClick = (suggestion: string) => {
    handleSubmitMessage(suggestion)
  }

  return (
    <div className="flex flex-col h-screen bg-mesh">
      {/* Ambient background blobs */}
      <div className="fixed top-20 left-1/4 w-96 h-96 bg-pacific-400/10 rounded-full blur-3xl pointer-events-none" />
      <div className="fixed bottom-20 right-1/4 w-80 h-80 bg-terracota-400/5 rounded-full blur-3xl pointer-events-none" />

      {/* Lawyer Modal */}
      <LawyerModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        lawyers={modalLawyers}
        legalArea={modalLegalArea}
        onTransferComplete={handleTransferComplete}
        isAuthenticated={isAuthenticated}
        onRequireAuth={() => {
          setAuthModalReason('lawyer')
          setShowAuthModal(true)
        }}
      />

      {/* Auth Modal */}
      <AuthModal
        isOpen={showAuthModal}
        onClose={() => setShowAuthModal(false)}
        onSuccess={() => setShowAuthModal(false)}
        login={login}
        register={register}
        reason={authModalReason}
      />

      {/* Glass Header */}
      <header className="glass-heavy shadow-glass sticky top-0 z-10">
        <div className="container flex h-16 items-center justify-between">
          <Link href="/">
            <LeiaLogo size="md" />
          </Link>
          <div className="flex items-center gap-4">
            {/* Question counter for unregistered users */}
            {!isAuthenticated && !authLoading && (
              <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full bg-pacific-50 border border-pacific-200">
                <span className="text-sm text-pacific-700">
                  {remainingQuestions > 0
                    ? `${remainingQuestions} consulta${remainingQuestions !== 1 ? 's' : ''} como invitado`
                    : 'Regístrate para continuar'}
                </span>
              </div>
            )}

            {/* User info for authenticated users */}
            {isAuthenticated && user && (
              <div className="hidden sm:flex items-center gap-3">
                <div className="flex items-center gap-2 px-3 py-1.5 rounded-full glass-button">
                  <User className="h-4 w-4 text-pacific-500" />
                  <span className="text-sm font-medium text-slate-600">{user.full_name || user.email}</span>
                </div>
                <button
                  onClick={logout}
                  className="text-xs text-slate-500 hover:text-slate-700 underline"
                >
                  Cerrar sesion
                </button>
              </div>
            )}

            {/* Login button for unregistered users */}
            {!isAuthenticated && !authLoading && (
              <Button
                variant="glass"
                size="sm"
                onClick={() => {
                  setAuthModalReason('limit')
                  setShowAuthModal(true)
                }}
              >
                <LogIn className="h-4 w-4 mr-2" />
                Ingresar
              </Button>
            )}

            <Button variant="glass" size="sm" asChild>
              <Link href="/">
                <ArrowLeft className="h-4 w-4 mr-2" />
                Volver
              </Link>
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex-1 overflow-hidden">
        <div className="container h-full max-w-4xl py-6">
          <div className="flex flex-col h-full">

            {/* PRE-CHAT WELCOME SCREEN */}
            {!chatStarted && (
              <div className="flex-1 flex flex-col items-center justify-center text-center px-4 -mt-8">
                <div className="mb-6 animate-fade-in opacity-0" style={{ animationDelay: '0ms', animationFillMode: 'forwards' }}>
                  <LeiaAvatar size="xl" animated />
                </div>

                <h1
                  className="text-4xl sm:text-5xl font-semibold text-slate-900 mb-3 animate-fade-in-up opacity-0"
                  style={{ animationDelay: '200ms', animationFillMode: 'forwards' }}
                >
                  Tu primer paso legal
                </h1>

                <p
                  className="text-lg text-slate-600 max-w-md mb-4 animate-fade-in-up opacity-0"
                  style={{ animationDelay: '400ms', animationFillMode: 'forwards' }}
                >
                  Cuentame tu situacion. Te oriento gratis y, si lo necesitas, te conecto con un abogado verificado.
                </p>

                {/* Remaining questions indicator for unregistered users */}
                {!isAuthenticated && !authLoading && (
                  <div
                    className={cn(
                      "max-w-md mx-auto p-3 rounded-xl mb-4 animate-fade-in opacity-0",
                      remainingQuestions <= 2
                        ? "bg-amber-50/80 border border-amber-200"
                        : "bg-pacific-50/80 border border-pacific-200"
                    )}
                    style={{ animationDelay: '450ms', animationFillMode: 'forwards' }}
                  >
                    <p className={cn(
                      "text-sm text-center",
                      remainingQuestions <= 2 ? "text-amber-700" : "text-pacific-700"
                    )}>
                      {remainingQuestions > 0 ? (
                        <>
                          Tienes <strong>{remainingQuestions}</strong> consulta{remainingQuestions !== 1 ? 's' : ''} como invitado.{' '}
                          <button
                            onClick={() => {
                              setAuthModalReason('limit')
                              setShowAuthModal(true)
                            }}
                            className="text-pacific-600 font-medium underline hover:text-pacific-700"
                          >
                            Crea tu cuenta
                          </button>
                          {' '}para consultas sin límite.
                        </>
                      ) : (
                        <>
                          <button
                            onClick={() => {
                              setAuthModalReason('limit')
                              setShowAuthModal(true)
                            }}
                            className="text-pacific-600 font-medium underline hover:text-pacific-700"
                          >
                            Crea tu cuenta
                          </button>
                          {' '}para seguir consultando con LEIA.
                        </>
                      )}
                    </p>
                  </div>
                )}

                {/* Disclaimer visible */}
                <div
                  className="max-w-md mx-auto p-3 rounded-xl bg-amber-50/80 border border-amber-200 mb-8 animate-fade-in opacity-0"
                  style={{ animationDelay: '500ms', animationFillMode: 'forwards' }}
                >
                  <div className="flex items-start gap-2">
                    <Scale className="h-4 w-4 text-amber-600 mt-0.5 flex-shrink-0" />
                    <p className="text-xs text-amber-800">
                      <strong>Aviso legal:</strong> LEIA es un asistente de orientacion que utiliza IA.
                      La informacion proporcionada es general y <strong>no constituye asesoria legal profesional</strong>.
                      Para casos especificos, consulta con un abogado.
                    </p>
                  </div>
                </div>

                <div
                  className="w-full max-w-sm animate-fade-in opacity-0"
                  style={{ animationDelay: '700ms', animationFillMode: 'forwards' }}
                >
                  <p className="text-xs text-slate-400 mb-3 uppercase tracking-wide">Consultas frecuentes</p>
                  <div className="flex flex-wrap justify-center gap-2">
                    {suggestions.map((suggestion, index) => (
                      <button
                        key={index}
                        onClick={() => handleSuggestionClick(suggestion)}
                        className="px-4 py-2 rounded-full text-sm text-slate-500 hover:text-slate-800 bg-white/50 hover:bg-white/80 border border-slate-200/50 hover:border-slate-300 transition-all duration-300"
                      >
                        {suggestion}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* CHAT AREA */}
            {chatStarted && (
              <div className="flex-1 overflow-y-auto mb-4 pr-2 space-y-4">
                {messages.map((message) => (
                  <div key={message.id}>
                    <div className={`flex gap-3 ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                      {message.role === 'assistant' && (
                        <div className="flex-shrink-0">
                          <LeiaAvatar size="sm" animated={false} />
                        </div>
                      )}

                      <div className={`flex-1 max-w-[80%] ${message.role === 'user' ? 'order-first' : ''}`}>
                        <div
                          className={cn(
                            "p-4 rounded-2xl",
                            message.role === 'user'
                              ? "bg-gradient-to-br from-pacific-500 to-pacific-600 text-white ml-auto shadow-lg shadow-pacific-500/25"
                              : "glass-card"
                          )}
                        >
                          <p className="whitespace-pre-wrap text-sm leading-relaxed">{message.content}</p>
                        </div>

                        {/* Lawyer Button - Solo cuando showLawyerButton es true */}
                        {message.role === 'assistant' && message.showLawyerButton && !message.content.includes('Tu caso ha sido enviado') && (
                          <div className="mt-4 p-4 rounded-xl bg-gradient-to-r from-pacific-50 to-white border border-pacific-100">
                            <p className="text-sm text-slate-600 mb-3">
                              📋 Tu situacion puede requerir asesoria profesional
                            </p>
                            <button
                              onClick={() => handleOpenLawyerModal(message.suggestedSpecialties?.length ? message.suggestedSpecialties : ['Derecho Civil'])}
                              disabled={loadingLawyers}
                              className="w-full p-3 bg-gradient-to-r from-pacific-500 to-pacific-600 hover:from-pacific-600 hover:to-pacific-700 text-white rounded-xl shadow-lg shadow-pacific-500/30 transition-all duration-300 hover:shadow-xl hover:-translate-y-0.5 flex items-center justify-center gap-3"
                            >
                              {loadingLawyers ? (
                                <>
                                  <Loader2 className="h-5 w-5 animate-spin" />
                                  <span className="font-medium">Buscando abogados...</span>
                                </>
                              ) : (
                                <>
                                  <Scale className="h-5 w-5" />
                                  <span className="font-medium">
                                    Ver abogados de {message.suggestedSpecialties?.[0] || 'tu caso'}
                                  </span>
                                  <ChevronRight className="h-5 w-5" />
                                </>
                              )}
                            </button>
                            <p className="text-xs text-slate-400 mt-2 text-center">Solicitar contacto es gratis</p>
                          </div>
                        )}

                        {/* Feedback Buttons */}
                        {message.role === 'assistant' && !message.content.includes('✅ Tu caso ha sido enviado') && (
                          <div className="mt-2 flex items-center gap-2">
                            <span className="text-xs text-slate-500">¿Te fue util?</span>
                            <button
                              onClick={() => handleFeedback(message.id, 'helpful')}
                              disabled={message.feedback !== undefined}
                              className={cn(
                                "p-1.5 rounded-lg transition-all duration-200 disabled:opacity-50",
                                message.feedback === 'helpful'
                                  ? "glass-button text-green-600"
                                  : "hover:bg-white/60 text-slate-400 hover:text-green-500"
                              )}
                              title="Util"
                            >
                              <ThumbsUp className="h-4 w-4" />
                            </button>
                            <button
                              onClick={() => handleFeedback(message.id, 'not_helpful')}
                              disabled={message.feedback !== undefined}
                              className={cn(
                                "p-1.5 rounded-lg transition-all duration-200 disabled:opacity-50",
                                message.feedback === 'not_helpful'
                                  ? "glass-button text-terracota-600"
                                  : "hover:bg-white/60 text-slate-400 hover:text-terracota-500"
                              )}
                              title="No util"
                            >
                              <ThumbsDown className="h-4 w-4" />
                            </button>
                            {message.feedback === 'helpful' && (
                              <span className="text-xs text-green-600 ml-2">¡Gracias!</span>
                            )}
                          </div>
                        )}

                        {/* Correction field */}
                        {showCorrectionFor === message.id && (
                          <div className="mt-3 p-4 glass-card rounded-xl border border-terracota-200/50">
                            <p className="text-xs text-slate-700 mb-2 font-medium">
                              ¿Que estuvo mal? Tu feedback nos ayuda a mejorar.
                            </p>
                            <textarea
                              value={correctionText}
                              onChange={(e) => setCorrectionText(e.target.value)}
                              placeholder="Ej: La informacion sobre plazos no es correcta..."
                              className="w-full px-3 py-2 text-sm glass-input rounded-xl resize-none focus:outline-none focus:ring-2 focus:ring-pacific-400"
                              rows={2}
                            />
                            <div className="flex gap-2 mt-3">
                              <Button
                                size="sm"
                                variant="pacific"
                                onClick={() => handleCorrectionSubmit(message.id)}
                                disabled={!correctionText.trim()}
                              >
                                Enviar
                              </Button>
                              <Button
                                size="sm"
                                variant="glass"
                                onClick={() => {
                                  setShowCorrectionFor(null)
                                  setCorrectionText('')
                                }}
                              >
                                Cancelar
                              </Button>
                            </div>
                          </div>
                        )}
                      </div>

                      {message.role === 'user' && (
                        <div className="flex-shrink-0 w-10 h-10 rounded-xl glass-card flex items-center justify-center">
                          <User className="h-5 w-5 text-slate-600" />
                        </div>
                      )}
                    </div>
                  </div>
                ))}

                {/* Loading indicator */}
                {isLoading && (
                  <div className="flex gap-3">
                    <div className="flex-shrink-0">
                      <LeiaAvatar size="sm" animated />
                    </div>
                    <div className="glass-card p-4 rounded-2xl">
                      <div className="flex gap-1.5">
                        <div className="w-2 h-2 bg-pacific-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                        <div className="w-2 h-2 bg-pacific-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                        <div className="w-2 h-2 bg-pacific-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                      </div>
                    </div>
                  </div>
                )}

                <div ref={messagesEndRef} />
              </div>
            )}

            {/* Input Form */}
            <div
              className={cn(
                "rounded-2xl p-2 transition-all duration-500",
                !chatStarted
                  ? "bg-white/40 border border-slate-200/50 animate-fade-in opacity-0"
                  : "glass-card",
                isFocused && "shadow-glass-lg glow-pacific bg-white/90"
              )}
              style={!chatStarted ? { animationDelay: '900ms', animationFillMode: 'forwards' } : {}}
            >
              <form onSubmit={handleSubmit} className="flex gap-2">
                <input
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onFocus={() => setIsFocused(true)}
                  onBlur={() => setIsFocused(false)}
                  placeholder={chatStarted ? "Escribe tu mensaje..." : "Cuentame, ¿en que puedo ayudarte?"}
                  disabled={isLoading}
                  className="flex-1 px-4 py-3 bg-transparent border-0 text-slate-800 placeholder:text-slate-400 focus:outline-none focus:ring-0 text-sm"
                />
                <Button
                  type="submit"
                  variant="pacific"
                  disabled={isLoading || !input.trim()}
                  className="rounded-xl shadow-lg shadow-pacific-500/25"
                >
                  {isLoading ? (
                    <Loader2 className="h-5 w-5 animate-spin" />
                  ) : (
                    <Send className="h-5 w-5" />
                  )}
                </Button>
              </form>
            </div>

            {/* Disclaimer */}
            <div className="mt-4 text-center">
              <p className="text-xs text-slate-500">
                LEIA proporciona orientacion general y no constituye asesoria legal.{' '}
                <Link href="/abogados" className="text-pacific-600 hover:underline">Contacta un abogado</Link>{' '}
                para casos especificos.
              </p>
              <p className="text-[10px] text-slate-400 mt-1">
                Al usar este servicio aceptas nuestros{' '}
                <Link href="/terminos" className="underline">Terminos</Link> y{' '}
                <Link href="/privacidad" className="underline">Privacidad</Link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default function ChatPage() {
  return (
    <Suspense fallback={<div className="flex items-center justify-center h-screen bg-mesh">Cargando...</div>}>
      <ChatContent />
    </Suspense>
  )
}
