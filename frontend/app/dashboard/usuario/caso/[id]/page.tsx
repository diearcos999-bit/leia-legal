'use client'

import { useState, useEffect } from 'react'
import { useParams, useRouter } from 'next/navigation'
import Link from 'next/link'
import { useAuth } from '@/lib/auth'
import { Button } from '@/components/ui/button'
import { RoleGuard, PageHeader } from '@/components/dashboard'
import { CaseChat } from '@/components/case-chat'
import {
  ArrowLeft,
  Briefcase,
  Clock,
  CheckCircle,
  XCircle,
  AlertCircle,
  Calendar,
  MapPin,
  FileText,
  User,
  Scale,
  Loader2,
  AlertTriangle,
  Phone,
  Video
} from 'lucide-react'
import { cn } from '@/lib/utils'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface CaseDetail {
  id: number
  case_number: string
  title: string
  summary?: string
  description?: string
  legal_area?: string
  sub_area?: string
  priority: 'low' | 'medium' | 'high' | 'urgent'
  status: string
  region?: string
  city?: string
  risk_level?: number
  risk_factors?: string[]
  extracted_facts?: string[]
  pending_questions?: string[]
  assigned_lawyer_id?: number
  created_at: string
  updated_at?: string
  transferred_at?: string
}

interface Transfer {
  id: number
  lawyer_id: number
  status: string
  user_message?: string
  lawyer_response?: string
  agreed_price?: number
  service_type?: string
  created_at: string
  accepted_at?: string
}

interface Lawyer {
  id: number
  name: string
  specialty: string
  rating?: number
  is_verified: boolean
}

interface CommunicationSettings {
  chat_enabled: boolean
  voice_enabled: boolean
  video_enabled: boolean
}

const statusConfig: Record<string, { label: string; color: string; icon: React.ElementType }> = {
  draft: { label: 'Borrador', color: 'bg-slate-100 text-slate-600', icon: Clock },
  ready: { label: 'Listo para transferir', color: 'bg-yellow-100 text-yellow-700', icon: AlertCircle },
  pending_consent: { label: 'Pendiente consentimiento', color: 'bg-orange-100 text-orange-700', icon: Clock },
  transferred: { label: 'Transferido - Esperando respuesta', color: 'bg-blue-100 text-blue-700', icon: Clock },
  in_progress: { label: 'En progreso', color: 'bg-pacific-100 text-pacific-700', icon: Briefcase },
  completed: { label: 'Completado', color: 'bg-green-100 text-green-700', icon: CheckCircle },
  cancelled: { label: 'Cancelado', color: 'bg-red-100 text-red-700', icon: XCircle },
  archived: { label: 'Archivado', color: 'bg-slate-100 text-slate-500', icon: Clock }
}

const priorityConfig: Record<string, { label: string; color: string }> = {
  low: { label: 'Baja', color: 'text-slate-500 bg-slate-100' },
  medium: { label: 'Media', color: 'text-yellow-700 bg-yellow-100' },
  high: { label: 'Alta', color: 'text-orange-700 bg-orange-100' },
  urgent: { label: 'Urgente', color: 'text-red-700 bg-red-100' }
}

export default function CasoDetailPage() {
  const params = useParams()
  const router = useRouter()
  const { token } = useAuth()
  const caseId = params.id as string

  const [caseDetail, setCaseDetail] = useState<CaseDetail | null>(null)
  const [transfers, setTransfers] = useState<Transfer[]>([])
  const [lawyer, setLawyer] = useState<Lawyer | null>(null)
  const [communicationSettings, setCommunicationSettings] = useState<CommunicationSettings | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchCaseData = async () => {
      if (!token || !caseId) return

      try {
        // Fetch case details
        const caseResponse = await fetch(`${API_URL}/api/cases/${caseId}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        })

        if (!caseResponse.ok) {
          setError('Caso no encontrado')
          setIsLoading(false)
          return
        }

        const caseData = await caseResponse.json()
        setCaseDetail(caseData)

        // Fetch transfers
        const transfersResponse = await fetch(`${API_URL}/api/cases/${caseId}/transfers`, {
          headers: { 'Authorization': `Bearer ${token}` }
        })

        if (transfersResponse.ok) {
          const transfersData = await transfersResponse.json()
          setTransfers(transfersData)

          // If there's an accepted transfer, fetch lawyer info
          const acceptedTransfer = transfersData.find((t: Transfer) => t.status === 'accepted')
          if (acceptedTransfer) {
            const lawyerResponse = await fetch(`${API_URL}/api/lawyers/${acceptedTransfer.lawyer_id}`, {
              headers: { 'Authorization': `Bearer ${token}` }
            })

            if (lawyerResponse.ok) {
              const lawyerData = await lawyerResponse.json()
              setLawyer(lawyerData)
            }
          }
        }

        setError(null)
      } catch (err) {
        setError('Error de conexión')
      } finally {
        setIsLoading(false)
      }
    }

    fetchCaseData()
  }, [token, caseId])

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('es-CL', {
      day: 'numeric',
      month: 'long',
      year: 'numeric'
    })
  }

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('es-CL', {
      style: 'currency',
      currency: 'CLP'
    }).format(price)
  }

  const handleCallRequest = (callType: 'voice' | 'video') => {
    // TODO: Implement call functionality
    console.log('Call request:', callType)
  }

  if (isLoading) {
    return (
      <RoleGuard allowedRole="user">
        <div className="flex items-center justify-center py-12">
          <Loader2 className="h-8 w-8 animate-spin text-pacific-500" />
        </div>
      </RoleGuard>
    )
  }

  if (error || !caseDetail) {
    return (
      <RoleGuard allowedRole="user">
        <div className="text-center py-12">
          <AlertTriangle className="h-12 w-12 mx-auto text-red-500 mb-4" />
          <p className="text-red-600">{error || 'Caso no encontrado'}</p>
          <Button variant="outline" className="mt-4" asChild>
            <Link href="/dashboard/usuario/mis-casos">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Volver a mis casos
            </Link>
          </Button>
        </div>
      </RoleGuard>
    )
  }

  const status = statusConfig[caseDetail.status] || statusConfig.draft
  const StatusIcon = status.icon
  const priority = priorityConfig[caseDetail.priority] || priorityConfig.medium
  const activeTransfer = transfers.find(t => t.status === 'accepted' || t.status === 'pending')

  return (
    <RoleGuard allowedRole="user">
      {/* Back button */}
      <Button variant="ghost" className="mb-4" asChild>
        <Link href="/dashboard/usuario/mis-casos">
          <ArrowLeft className="h-4 w-4 mr-2" />
          Volver a mis casos
        </Link>
      </Button>

      {/* Header */}
      <div className="glass-card rounded-xl p-6 mb-6">
        <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className="text-sm font-mono text-slate-500">
                {caseDetail.case_number}
              </span>
              <span className={cn(
                'px-2 py-0.5 rounded-full text-xs font-medium',
                status.color
              )}>
                <StatusIcon className="h-3 w-3 inline mr-1" />
                {status.label}
              </span>
            </div>
            <h1 className="text-2xl font-bold text-slate-900 mb-2">
              {caseDetail.title}
            </h1>
            <div className="flex flex-wrap items-center gap-3 text-sm text-slate-600">
              {caseDetail.legal_area && (
                <span className="flex items-center gap-1">
                  <Scale className="h-4 w-4" />
                  {caseDetail.legal_area}
                  {caseDetail.sub_area && ` - ${caseDetail.sub_area}`}
                </span>
              )}
              {(caseDetail.region || caseDetail.city) && (
                <span className="flex items-center gap-1">
                  <MapPin className="h-4 w-4" />
                  {[caseDetail.city, caseDetail.region].filter(Boolean).join(', ')}
                </span>
              )}
              <span className="flex items-center gap-1">
                <Calendar className="h-4 w-4" />
                Creado {formatDate(caseDetail.created_at)}
              </span>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <span className={cn(
              'px-3 py-1 rounded-full text-sm font-medium',
              priority.color
            )}>
              Prioridad {priority.label}
            </span>
            {caseDetail.risk_level && (
              <span className={cn(
                'px-3 py-1 rounded-full text-sm font-medium',
                caseDetail.risk_level >= 7
                  ? 'bg-red-100 text-red-700'
                  : caseDetail.risk_level >= 4
                  ? 'bg-yellow-100 text-yellow-700'
                  : 'bg-green-100 text-green-700'
              )}>
                Riesgo: {caseDetail.risk_level}/10
              </span>
            )}
          </div>
        </div>
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Main content */}
        <div className="lg:col-span-2 space-y-6">
          {/* Summary */}
          {caseDetail.summary && (
            <div className="glass-card rounded-xl p-6">
              <h2 className="font-semibold text-slate-900 mb-3">Resumen del Caso</h2>
              <p className="text-slate-600">{caseDetail.summary}</p>
            </div>
          )}

          {/* Facts */}
          {caseDetail.extracted_facts && caseDetail.extracted_facts.length > 0 && (
            <div className="glass-card rounded-xl p-6">
              <h2 className="font-semibold text-slate-900 mb-3">Hechos Principales</h2>
              <ul className="space-y-2">
                {caseDetail.extracted_facts.map((fact, index) => (
                  <li key={index} className="flex items-start gap-2 text-slate-600">
                    <CheckCircle className="h-4 w-4 text-pacific-500 mt-1 flex-shrink-0" />
                    {fact}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Risk factors */}
          {caseDetail.risk_factors && caseDetail.risk_factors.length > 0 && (
            <div className="glass-card rounded-xl p-6">
              <h2 className="font-semibold text-slate-900 mb-3">Factores de Riesgo</h2>
              <ul className="space-y-2">
                {caseDetail.risk_factors.map((factor, index) => (
                  <li key={index} className="flex items-start gap-2 text-slate-600">
                    <AlertTriangle className="h-4 w-4 text-orange-500 mt-1 flex-shrink-0" />
                    {factor}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Chat with lawyer */}
          {activeTransfer && activeTransfer.status === 'accepted' && (
            <div className="glass-card rounded-xl p-6">
              <h2 className="font-semibold text-slate-900 mb-4">
                Chat con tu Abogado
              </h2>
              <CaseChat
                transferId={activeTransfer.id}
                caseNumber={caseDetail.case_number}
                participantType="user"
                participantName={lawyer?.name}
                communicationSettings={communicationSettings || undefined}
                onCallRequest={handleCallRequest}
              />
            </div>
          )}

          {/* Waiting for lawyer response */}
          {activeTransfer && activeTransfer.status === 'pending' && (
            <div className="glass-card rounded-xl p-6 bg-blue-50 border-blue-200">
              <div className="flex items-start gap-4">
                <Clock className="h-8 w-8 text-blue-500" />
                <div>
                  <h3 className="font-semibold text-slate-900 mb-2">
                    Esperando respuesta del abogado
                  </h3>
                  <p className="text-slate-600 mb-2">
                    Tu caso ha sido enviado al abogado. Te notificaremos cuando responda.
                  </p>
                  {activeTransfer.user_message && (
                    <div className="mt-3 p-3 bg-white rounded-lg">
                      <p className="text-sm text-slate-500 mb-1">Tu mensaje:</p>
                      <p className="text-slate-700">{activeTransfer.user_message}</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Need to select lawyer */}
          {caseDetail.status === 'ready' && !activeTransfer && (
            <div className="glass-card rounded-xl p-6 bg-yellow-50 border-yellow-200">
              <div className="flex items-start gap-4">
                <AlertCircle className="h-8 w-8 text-yellow-500" />
                <div>
                  <h3 className="font-semibold text-slate-900 mb-2">
                    Selecciona un abogado
                  </h3>
                  <p className="text-slate-600 mb-4">
                    Tu caso está listo para ser transferido. Selecciona un abogado para continuar.
                  </p>
                  <Button variant="pacific" asChild>
                    <Link href="/abogados">
                      Buscar Abogado
                    </Link>
                  </Button>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Lawyer info */}
          {lawyer && (
            <div className="glass-card rounded-xl p-6">
              <h2 className="font-semibold text-slate-900 mb-4">Tu Abogado</h2>
              <div className="flex items-center gap-3 mb-4">
                <div className="w-12 h-12 rounded-full bg-pacific-100 flex items-center justify-center">
                  <User className="h-6 w-6 text-pacific-600" />
                </div>
                <div>
                  <p className="font-medium text-slate-900">{lawyer.name}</p>
                  <p className="text-sm text-slate-500">{lawyer.specialty}</p>
                </div>
              </div>
              {lawyer.is_verified && (
                <div className="flex items-center gap-2 text-sm text-green-600 mb-3">
                  <CheckCircle className="h-4 w-4" />
                  Abogado verificado
                </div>
              )}
              {lawyer.rating && (
                <div className="flex items-center gap-1 text-sm text-slate-600">
                  <span className="text-yellow-500">★</span>
                  {lawyer.rating.toFixed(1)}
                </div>
              )}
              {activeTransfer?.agreed_price && (
                <div className="mt-4 pt-4 border-t border-slate-200">
                  <p className="text-sm text-slate-500">Precio acordado</p>
                  <p className="text-lg font-semibold text-slate-900">
                    {formatPrice(activeTransfer.agreed_price)}
                  </p>
                </div>
              )}
            </div>
          )}

          {/* Pending questions */}
          {caseDetail.pending_questions && caseDetail.pending_questions.length > 0 && (
            <div className="glass-card rounded-xl p-6">
              <h2 className="font-semibold text-slate-900 mb-3">Preguntas Pendientes</h2>
              <ul className="space-y-2">
                {caseDetail.pending_questions.map((question, index) => (
                  <li key={index} className="text-sm text-slate-600 flex items-start gap-2">
                    <span className="text-pacific-500">•</span>
                    {question}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Timeline placeholder */}
          <div className="glass-card rounded-xl p-6">
            <h2 className="font-semibold text-slate-900 mb-3">Historial</h2>
            <div className="space-y-3">
              <div className="flex items-start gap-3">
                <div className="w-2 h-2 rounded-full bg-pacific-500 mt-2" />
                <div>
                  <p className="text-sm text-slate-900">Caso creado</p>
                  <p className="text-xs text-slate-500">{formatDate(caseDetail.created_at)}</p>
                </div>
              </div>
              {caseDetail.transferred_at && (
                <div className="flex items-start gap-3">
                  <div className="w-2 h-2 rounded-full bg-blue-500 mt-2" />
                  <div>
                    <p className="text-sm text-slate-900">Caso transferido</p>
                    <p className="text-xs text-slate-500">{formatDate(caseDetail.transferred_at)}</p>
                  </div>
                </div>
              )}
              {activeTransfer?.accepted_at && (
                <div className="flex items-start gap-3">
                  <div className="w-2 h-2 rounded-full bg-green-500 mt-2" />
                  <div>
                    <p className="text-sm text-slate-900">Abogado aceptó el caso</p>
                    <p className="text-xs text-slate-500">{formatDate(activeTransfer.accepted_at)}</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </RoleGuard>
  )
}
