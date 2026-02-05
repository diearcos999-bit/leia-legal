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
  Video,
  Mail,
  Download,
  MessageSquare
} from 'lucide-react'
import { cn } from '@/lib/utils'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface CaseData {
  id: number
  case_number: string
  title: string
  summary?: string
  description?: string
  legal_area?: string
  sub_area?: string
  priority: string
  status: string
  region?: string
  city?: string
  risk_level?: number
  risk_factors?: string[]
  extracted_facts?: string[]
  pending_questions?: string[]
  created_at: string
}

interface TransferData {
  id: number
  status: string
  user_message?: string
  agreed_price?: number
  service_type?: string
  created_at: string
  accepted_at?: string
}

interface ContactInfo {
  name?: string
  email?: string
}

interface ChatMessage {
  role: string
  content: string
  created_at: string
}

interface Document {
  id: number
  filename: string
  file_type?: string
  file_size?: number
  description?: string
  created_at: string
}

interface CaseFullData {
  case: CaseData
  transfer: TransferData
  contact_info?: ContactInfo
  chat_history: ChatMessage[]
  documents: Document[]
}

const statusConfig: Record<string, { label: string; color: string; icon: React.ElementType }> = {
  draft: { label: 'Borrador', color: 'bg-slate-100 text-slate-600', icon: Clock },
  ready: { label: 'Listo', color: 'bg-yellow-100 text-yellow-700', icon: AlertCircle },
  pending_consent: { label: 'Pendiente', color: 'bg-orange-100 text-orange-700', icon: Clock },
  transferred: { label: 'Pendiente respuesta', color: 'bg-blue-100 text-blue-700', icon: Clock },
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

export default function CasoLawyerPage() {
  const params = useParams()
  const router = useRouter()
  const { token } = useAuth()
  const caseId = params.id as string

  const [caseData, setCaseData] = useState<CaseFullData | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [showLeiaChat, setShowLeiaChat] = useState(false)

  useEffect(() => {
    const fetchCaseData = async () => {
      if (!token || !caseId) return

      try {
        const response = await fetch(`${API_URL}/api/cases/lawyer/case/${caseId}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        })

        if (!response.ok) {
          if (response.status === 403) {
            setError('No tienes acceso a este caso')
          } else {
            setError('Caso no encontrado')
          }
          setIsLoading(false)
          return
        }

        const data = await response.json()
        setCaseData(data)
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

  const formatFileSize = (bytes?: number) => {
    if (!bytes) return ''
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
  }

  const handleCallRequest = (callType: 'voice' | 'video') => {
    // TODO: Implement call functionality
    console.log('Call request:', callType)
  }

  if (isLoading) {
    return (
      <RoleGuard allowedRole="lawyer">
        <div className="flex items-center justify-center py-12">
          <Loader2 className="h-8 w-8 animate-spin text-pacific-500" />
        </div>
      </RoleGuard>
    )
  }

  if (error || !caseData) {
    return (
      <RoleGuard allowedRole="lawyer">
        <div className="text-center py-12">
          <AlertTriangle className="h-12 w-12 mx-auto text-red-500 mb-4" />
          <p className="text-red-600">{error || 'Caso no encontrado'}</p>
          <Button variant="outline" className="mt-4" asChild>
            <Link href="/dashboard/profesional/casos">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Volver a mis casos
            </Link>
          </Button>
        </div>
      </RoleGuard>
    )
  }

  const { case: caseDetail, transfer, contact_info, chat_history, documents } = caseData
  const status = statusConfig[caseDetail.status] || statusConfig.draft
  const StatusIcon = status.icon
  const priority = priorityConfig[caseDetail.priority] || priorityConfig.medium

  return (
    <RoleGuard allowedRole="lawyer">
      {/* Back button */}
      <Button variant="ghost" className="mb-4" asChild>
        <Link href="/dashboard/profesional/casos">
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
                Recibido {formatDate(transfer.created_at)}
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

          {/* Client message */}
          {transfer.user_message && (
            <div className="glass-card rounded-xl p-6">
              <h2 className="font-semibold text-slate-900 mb-3">Mensaje del Cliente</h2>
              <div className="p-4 bg-slate-50 rounded-lg">
                <p className="text-slate-700">{transfer.user_message}</p>
              </div>
            </div>
          )}

          {/* Facts */}
          {caseDetail.extracted_facts && caseDetail.extracted_facts.length > 0 && (
            <div className="glass-card rounded-xl p-6">
              <h2 className="font-semibold text-slate-900 mb-3">Hechos Extraídos</h2>
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

          {/* LEIA Chat History */}
          {chat_history.length > 0 && (
            <div className="glass-card rounded-xl p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="font-semibold text-slate-900">
                  Conversación con LEIA
                </h2>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setShowLeiaChat(!showLeiaChat)}
                >
                  {showLeiaChat ? 'Ocultar' : 'Mostrar'} historial
                </Button>
              </div>
              {showLeiaChat && (
                <div className="space-y-3 max-h-96 overflow-y-auto">
                  {chat_history.map((msg, index) => (
                    <div
                      key={index}
                      className={cn(
                        'p-3 rounded-lg',
                        msg.role === 'user'
                          ? 'bg-slate-100 ml-8'
                          : 'bg-pacific-50 mr-8'
                      )}
                    >
                      <p className="text-xs text-slate-500 mb-1">
                        {msg.role === 'user' ? 'Cliente' : 'LEIA'}
                      </p>
                      <p className="text-sm text-slate-700">{msg.content}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Chat with client */}
          {transfer.status === 'accepted' && (
            <div className="glass-card rounded-xl p-6">
              <h2 className="font-semibold text-slate-900 mb-4">
                Chat con el Cliente
              </h2>
              <CaseChat
                transferId={transfer.id}
                caseNumber={caseDetail.case_number}
                participantType="lawyer"
                participantName={contact_info?.name}
                onCallRequest={handleCallRequest}
              />
            </div>
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Client info */}
          {contact_info && (
            <div className="glass-card rounded-xl p-6">
              <h2 className="font-semibold text-slate-900 mb-4">Información del Cliente</h2>
              <div className="space-y-3">
                {contact_info.name && (
                  <div className="flex items-center gap-3">
                    <User className="h-5 w-5 text-slate-400" />
                    <span className="text-slate-700">{contact_info.name}</span>
                  </div>
                )}
                {contact_info.email && (
                  <div className="flex items-center gap-3">
                    <Mail className="h-5 w-5 text-slate-400" />
                    <a
                      href={`mailto:${contact_info.email}`}
                      className="text-pacific-600 hover:underline"
                    >
                      {contact_info.email}
                    </a>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Documents */}
          {documents.length > 0 && (
            <div className="glass-card rounded-xl p-6">
              <h2 className="font-semibold text-slate-900 mb-4">Documentos</h2>
              <div className="space-y-2">
                {documents.map((doc) => (
                  <div
                    key={doc.id}
                    className="flex items-center justify-between p-3 bg-slate-50 rounded-lg"
                  >
                    <div className="flex items-center gap-3">
                      <FileText className="h-5 w-5 text-slate-400" />
                      <div>
                        <p className="text-sm font-medium text-slate-700 truncate max-w-[150px]">
                          {doc.filename}
                        </p>
                        <p className="text-xs text-slate-500">
                          {formatFileSize(doc.file_size)}
                        </p>
                      </div>
                    </div>
                    <Button variant="ghost" size="sm">
                      <Download className="h-4 w-4" />
                    </Button>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Case details */}
          <div className="glass-card rounded-xl p-6">
            <h2 className="font-semibold text-slate-900 mb-4">Detalles del Caso</h2>
            <div className="space-y-3 text-sm">
              {transfer.service_type && (
                <div className="flex justify-between">
                  <span className="text-slate-500">Tipo de servicio</span>
                  <span className="text-slate-700">{transfer.service_type}</span>
                </div>
              )}
              {transfer.agreed_price && (
                <div className="flex justify-between">
                  <span className="text-slate-500">Precio acordado</span>
                  <span className="font-medium text-slate-900">
                    {formatPrice(transfer.agreed_price)}
                  </span>
                </div>
              )}
              {transfer.accepted_at && (
                <div className="flex justify-between">
                  <span className="text-slate-500">Aceptado</span>
                  <span className="text-slate-700">{formatDate(transfer.accepted_at)}</span>
                </div>
              )}
            </div>
          </div>

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
        </div>
      </div>
    </RoleGuard>
  )
}
