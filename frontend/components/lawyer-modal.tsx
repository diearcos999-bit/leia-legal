'use client'

import { useState, useEffect } from 'react'
import { X, Star, MapPin, Clock, Shield, CheckCircle2, FileText, MessageSquare, User, ChevronRight, ChevronLeft, Loader2, Scale, BadgeCheck } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface Lawyer {
  id: number
  name: string
  specialty: string
  rating: number
  reviews_count: number
  location: string
  price_display: string
  price_min?: number
  price_max?: number
  is_verified: boolean
  match_score?: number
  experience?: string
  cases_completed?: number
  success_rate?: number
  description?: string
  image?: string
  avg_response_time?: string
}

interface LawyerModalProps {
  isOpen: boolean
  onClose: () => void
  lawyers: Lawyer[]
  legalArea: string
  onTransferComplete?: (lawyerId: number) => void
}

type Step = 'select' | 'consent' | 'confirmation'

interface ConsentState {
  shareChat: boolean
  shareContact: boolean
  shareDocuments: boolean
}

interface ContactForm {
  name: string
  whatsapp: string
  when: 'today' | 'tomorrow' | 'anytime'
}

export function LawyerModal({ isOpen, onClose, lawyers, legalArea, onTransferComplete }: LawyerModalProps) {
  const [step, setStep] = useState<Step>('select')
  const [selectedLawyer, setSelectedLawyer] = useState<Lawyer | null>(null)
  const [consent, setConsent] = useState<ConsentState>({
    shareChat: false,
    shareContact: false,
    shareDocuments: false
  })
  const [contactForm, setContactForm] = useState<ContactForm>({
    name: '',
    whatsapp: '',
    when: 'today'
  })
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [lawyerDetails, setLawyerDetails] = useState<Lawyer | null>(null)
  const [loadingDetails, setLoadingDetails] = useState(false)

  // Reset state when modal opens
  useEffect(() => {
    if (isOpen) {
      setStep('select')
      setSelectedLawyer(null)
      setConsent({ shareChat: false, shareContact: false, shareDocuments: false })
    }
  }, [isOpen])

  // Fetch lawyer details when selected
  const fetchLawyerDetails = async (lawyerId: number) => {
    setLoadingDetails(true)
    try {
      const response = await fetch(`${API_URL}/api/lawyers/${lawyerId}/full`)
      if (response.ok) {
        const data = await response.json()
        setLawyerDetails(data)
      }
    } catch (error) {
      console.error('Error fetching lawyer details:', error)
    } finally {
      setLoadingDetails(false)
    }
  }

  const handleSelectLawyer = (lawyer: Lawyer) => {
    setSelectedLawyer(lawyer)
    fetchLawyerDetails(lawyer.id)
    setStep('consent')
  }

  const handleBack = () => {
    if (step === 'consent') {
      setStep('select')
      setSelectedLawyer(null)
    } else if (step === 'confirmation') {
      setStep('consent')
    }
  }

  const handleConsent = async () => {
    if (!canProceed) return

    setIsSubmitting(true)

    // Simulate API call for transfer
    await new Promise(resolve => setTimeout(resolve, 1500))

    setIsSubmitting(false)
    setStep('confirmation')

    if (onTransferComplete && selectedLawyer) {
      onTransferComplete(selectedLawyer.id)
    }
  }

  const canProceed = contactForm.name.trim() !== '' && contactForm.whatsapp.trim() !== ''

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="relative w-full max-w-2xl max-h-[90vh] mx-4 bg-white rounded-2xl shadow-2xl overflow-hidden flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-200 bg-gradient-to-r from-pacific-50 to-white">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-pacific-100 rounded-xl">
              <Scale className="h-5 w-5 text-pacific-600" />
            </div>
            <div>
              <h2 className="text-lg font-semibold text-slate-800">
                {step === 'select' && 'Abogados Recomendados'}
                {step === 'consent' && 'Compartir tu Caso'}
                {step === 'confirmation' && 'Solicitud Enviada'}
              </h2>
              <p className="text-sm text-slate-500">
                {step === 'select' && `Especialistas en ${legalArea}`}
                {step === 'consent' && selectedLawyer?.name}
                {step === 'confirmation' && 'Tu caso ha sido transferido'}
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-slate-100 rounded-xl transition-colors"
          >
            <X className="h-5 w-5 text-slate-500" />
          </button>
        </div>

        {/* Progress Steps */}
        <div className="px-6 py-3 bg-slate-50 border-b border-slate-200">
          <div className="flex items-center justify-center gap-2">
            {['select', 'consent', 'confirmation'].map((s, i) => (
              <div key={s} className="flex items-center">
                <div className={cn(
                  "w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium transition-colors",
                  step === s
                    ? "bg-pacific-500 text-white"
                    : ['select', 'consent', 'confirmation'].indexOf(step) > i
                      ? "bg-green-500 text-white"
                      : "bg-slate-200 text-slate-500"
                )}>
                  {['select', 'consent', 'confirmation'].indexOf(step) > i ? (
                    <CheckCircle2 className="h-5 w-5" />
                  ) : (
                    i + 1
                  )}
                </div>
                {i < 2 && (
                  <div className={cn(
                    "w-12 h-1 mx-1 rounded-full",
                    ['select', 'consent', 'confirmation'].indexOf(step) > i
                      ? "bg-green-500"
                      : "bg-slate-200"
                  )} />
                )}
              </div>
            ))}
          </div>
          <div className="flex justify-center gap-8 mt-2 text-xs text-slate-500">
            <span>Elegir</span>
            <span>Consentir</span>
            <span>Confirmar</span>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6">
          {/* Step 1: Select Lawyer */}
          {step === 'select' && (
            <div className="space-y-4">
              {lawyers.length === 0 ? (
                <div className="text-center py-8 text-slate-500">
                  No hay abogados disponibles en este momento
                </div>
              ) : (
                lawyers.map((lawyer) => (
                  <div
                    key={lawyer.id}
                    onClick={() => handleSelectLawyer(lawyer)}
                    className="p-4 border border-slate-200 rounded-xl hover:border-pacific-300 hover:shadow-lg cursor-pointer transition-all duration-300 group"
                  >
                    <div className="flex gap-4">
                      {/* Avatar */}
                      <div className="flex-shrink-0">
                        {lawyer.image ? (
                          <img
                            src={lawyer.image}
                            alt={lawyer.name}
                            className="w-16 h-16 rounded-xl object-cover"
                          />
                        ) : (
                          <div className="w-16 h-16 rounded-xl bg-gradient-to-br from-pacific-400 to-pacific-600 flex items-center justify-center text-white text-2xl font-semibold">
                            {lawyer.name.charAt(0)}
                          </div>
                        )}
                      </div>

                      {/* Info */}
                      <div className="flex-1 min-w-0">
                        <div className="flex items-start justify-between">
                          <div>
                            <div className="flex items-center gap-2">
                              <h3 className="font-semibold text-slate-800 group-hover:text-pacific-600 transition-colors">
                                {lawyer.name}
                              </h3>
                              {lawyer.is_verified && (
                                <BadgeCheck className="h-5 w-5 text-green-500" />
                              )}
                            </div>
                            <p className="text-sm text-pacific-600 font-medium">{lawyer.specialty}</p>
                          </div>
                          {lawyer.match_score && (
                            <span className="px-2 py-1 bg-pacific-100 text-pacific-700 text-xs font-medium rounded-full">
                              {lawyer.match_score}% match
                            </span>
                          )}
                        </div>

                        <div className="flex flex-wrap items-center gap-4 mt-2 text-sm text-slate-500">
                          <span className="flex items-center gap-1">
                            <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                            <span className="font-medium text-slate-700">{lawyer.rating}</span>
                            <span>({lawyer.reviews_count} reseñas)</span>
                          </span>
                          <span className="flex items-center gap-1">
                            <MapPin className="h-4 w-4" />
                            {lawyer.location?.split(',')[0]}
                          </span>
                          {lawyer.experience && (
                            <span className="flex items-center gap-1">
                              <Clock className="h-4 w-4" />
                              {lawyer.experience}
                            </span>
                          )}
                        </div>

                        <div className="flex items-center justify-between mt-3 pt-3 border-t border-slate-100">
                          <div>
                            <span className="text-lg font-bold text-slate-800">{lawyer.price_display}</span>
                            <span className="text-xs text-slate-500 ml-1">consulta inicial</span>
                          </div>
                          <div className="flex items-center gap-1 text-pacific-600 font-medium text-sm group-hover:translate-x-1 transition-transform">
                            Seleccionar <ChevronRight className="h-4 w-4" />
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          )}

          {/* Step 2: Contact Form (Simplified) */}
          {step === 'consent' && selectedLawyer && (
            <div className="space-y-6">
              {/* Selected Lawyer Summary */}
              <div className="p-4 bg-pacific-50 rounded-xl border border-pacific-100">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-pacific-400 to-pacific-600 flex items-center justify-center text-white text-lg font-semibold">
                    {selectedLawyer.name.charAt(0)}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <h3 className="font-semibold text-slate-800">{selectedLawyer.name}</h3>
                      {selectedLawyer.is_verified && (
                        <BadgeCheck className="h-4 w-4 text-green-500" />
                      )}
                    </div>
                    <p className="text-sm text-pacific-600">{selectedLawyer.specialty}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-lg font-bold text-slate-800">{selectedLawyer.price_display}</p>
                    <p className="text-xs text-slate-500">primera consulta</p>
                  </div>
                </div>
              </div>

              {/* Simple Contact Form */}
              <div>
                <h3 className="font-semibold text-slate-800 mb-4">
                  Para que {selectedLawyer.name.split(' ')[0]} te contacte:
                </h3>

                <div className="space-y-4">
                  {/* Name */}
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">
                      Tu nombre
                    </label>
                    <input
                      type="text"
                      value={contactForm.name}
                      onChange={(e) => setContactForm(prev => ({ ...prev, name: e.target.value }))}
                      placeholder="Ej: Maria Garcia"
                      className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-pacific-500 focus:ring-2 focus:ring-pacific-500/20 outline-none transition-all"
                    />
                  </div>

                  {/* WhatsApp */}
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">
                      WhatsApp
                    </label>
                    <input
                      type="tel"
                      value={contactForm.whatsapp}
                      onChange={(e) => setContactForm(prev => ({ ...prev, whatsapp: e.target.value }))}
                      placeholder="+56 9 1234 5678"
                      className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-pacific-500 focus:ring-2 focus:ring-pacific-500/20 outline-none transition-all"
                    />
                  </div>

                  {/* When */}
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-2">
                      ¿Cuando te puede contactar?
                    </label>
                    <div className="grid grid-cols-3 gap-2">
                      {[
                        { value: 'today', label: 'Hoy' },
                        { value: 'tomorrow', label: 'Manana' },
                        { value: 'anytime', label: 'Cuando pueda' }
                      ].map((option) => (
                        <button
                          key={option.value}
                          type="button"
                          onClick={() => setContactForm(prev => ({ ...prev, when: option.value as ContactForm['when'] }))}
                          className={cn(
                            "py-3 px-4 rounded-xl border-2 font-medium text-sm transition-all",
                            contactForm.when === option.value
                              ? "border-pacific-500 bg-pacific-50 text-pacific-700"
                              : "border-slate-200 text-slate-600 hover:border-slate-300"
                          )}
                        >
                          {option.label}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Privacy Note */}
                <div className="mt-6 p-3 bg-slate-50 rounded-lg flex items-start gap-2">
                  <Shield className="h-5 w-5 text-pacific-500 flex-shrink-0 mt-0.5" />
                  <p className="text-xs text-slate-500">
                    Solo compartiremos tu contacto con este abogado. Puedes cancelar en cualquier momento.
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Step 3: Confirmation */}
          {step === 'confirmation' && selectedLawyer && (
            <div className="text-center py-6">
              <div className="w-20 h-20 mx-auto mb-6 bg-green-100 rounded-full flex items-center justify-center">
                <CheckCircle2 className="h-10 w-10 text-green-500" />
              </div>

              <h3 className="text-2xl font-semibold text-slate-800 mb-2">
                ¡Listo, {contactForm.name.split(' ')[0]}!
              </h3>
              <p className="text-slate-500 mb-6">
                {selectedLawyer.name.split(' ')[0]} te contactara {contactForm.when === 'today' ? 'hoy' : contactForm.when === 'tomorrow' ? 'manana' : 'pronto'} por WhatsApp
              </p>

              {/* Lawyer Card */}
              <div className="max-w-sm mx-auto p-4 bg-pacific-50 rounded-xl mb-6 border border-pacific-100">
                <div className="flex items-center gap-3">
                  <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-pacific-400 to-pacific-600 flex items-center justify-center text-white text-xl font-semibold">
                    {selectedLawyer.name.charAt(0)}
                  </div>
                  <div className="text-left flex-1">
                    <div className="flex items-center gap-2">
                      <h4 className="font-semibold text-slate-800">{selectedLawyer.name}</h4>
                      {selectedLawyer.is_verified && (
                        <BadgeCheck className="h-4 w-4 text-green-500" />
                      )}
                    </div>
                    <p className="text-sm text-pacific-600">{selectedLawyer.specialty}</p>
                  </div>
                </div>
              </div>

              {/* Response Time */}
              <div className="inline-flex items-center gap-2 px-4 py-2 bg-green-50 rounded-full text-green-700 mb-6">
                <Clock className="h-5 w-5" />
                <span className="font-medium">
                  {contactForm.when === 'today' ? 'Te contactara antes de las 20:00' :
                   contactForm.when === 'tomorrow' ? 'Te contactara manana antes del mediodia' :
                   'Te contactara en menos de 24 horas'}
                </span>
              </div>

              {/* Guarantee */}
              <div className="max-w-sm mx-auto p-4 bg-slate-50 rounded-xl border border-slate-100">
                <div className="flex items-start gap-3">
                  <Shield className="h-5 w-5 text-pacific-500 flex-shrink-0 mt-0.5" />
                  <p className="text-sm text-slate-600 text-left">
                    Si no te contacta, te conectamos con otro abogado <strong>sin costo adicional</strong>.
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="px-6 py-4 border-t border-slate-200 bg-slate-50">
          <div className="flex items-center justify-between">
            {step !== 'select' && step !== 'confirmation' && (
              <Button
                variant="ghost"
                onClick={handleBack}
                className="text-slate-600"
              >
                <ChevronLeft className="h-4 w-4 mr-1" />
                Volver
              </Button>
            )}

            {step === 'select' && (
              <p className="text-sm text-slate-500">
                {lawyers.length} abogado{lawyers.length !== 1 ? 's' : ''} disponible{lawyers.length !== 1 ? 's' : ''}
              </p>
            )}

            {step === 'consent' && (
              <Button
                onClick={handleConsent}
                disabled={!canProceed || isSubmitting}
                className="bg-pacific-500 hover:bg-pacific-600 text-white ml-auto"
              >
                {isSubmitting ? (
                  <>
                    <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                    Enviando...
                  </>
                ) : (
                  <>
                    Enviar solicitud
                    <ChevronRight className="h-4 w-4 ml-1" />
                  </>
                )}
              </Button>
            )}

            {step === 'confirmation' && (
              <Button
                onClick={onClose}
                className="bg-pacific-500 hover:bg-pacific-600 text-white ml-auto"
              >
                Entendido
              </Button>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
