'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { useAuth } from '@/lib/auth'
import { Button } from '@/components/ui/button'
import { RoleGuard, PageHeader, EmptyState } from '@/components/dashboard'
import {
  Briefcase,
  Clock,
  CheckCircle,
  XCircle,
  AlertCircle,
  ArrowRight,
  MessageSquare,
  Loader2,
  Filter
} from 'lucide-react'
import { cn } from '@/lib/utils'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface Case {
  id: number
  case_number: string
  title: string
  summary?: string
  legal_area?: string
  priority: 'low' | 'medium' | 'high' | 'urgent'
  status: string
  region?: string
  city?: string
  created_at: string
  updated_at?: string
  assigned_lawyer_id?: number
}

interface CaseWithDetails extends Case {
  lawyer_name?: string
  unread_messages: number
  last_message?: {
    content: string
    sender_type: string
    created_at: string
  }
  transfer_status?: string
}

const statusConfig: Record<string, { label: string; color: string; icon: React.ElementType }> = {
  draft: { label: 'Borrador', color: 'bg-slate-100 text-slate-600', icon: Clock },
  ready: { label: 'Listo para transferir', color: 'bg-yellow-100 text-yellow-700', icon: AlertCircle },
  pending_consent: { label: 'Pendiente consentimiento', color: 'bg-orange-100 text-orange-700', icon: Clock },
  transferred: { label: 'Transferido', color: 'bg-blue-100 text-blue-700', icon: Clock },
  in_progress: { label: 'En progreso', color: 'bg-pacific-100 text-pacific-700', icon: Briefcase },
  completed: { label: 'Completado', color: 'bg-green-100 text-green-700', icon: CheckCircle },
  cancelled: { label: 'Cancelado', color: 'bg-red-100 text-red-700', icon: XCircle },
  archived: { label: 'Archivado', color: 'bg-slate-100 text-slate-500', icon: Clock }
}

const priorityConfig: Record<string, { label: string; color: string }> = {
  low: { label: 'Baja', color: 'text-slate-500' },
  medium: { label: 'Media', color: 'text-yellow-600' },
  high: { label: 'Alta', color: 'text-orange-600' },
  urgent: { label: 'Urgente', color: 'text-red-600' }
}

export default function MisCasosPage() {
  const { token } = useAuth()
  const [cases, setCases] = useState<CaseWithDetails[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [statusFilter, setStatusFilter] = useState<string | null>(null)

  useEffect(() => {
    const fetchCases = async () => {
      if (!token) return

      try {
        const url = statusFilter
          ? `${API_URL}/api/cases/?status_filter=${statusFilter}`
          : `${API_URL}/api/cases/`

        const response = await fetch(url, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })

        if (response.ok) {
          const data = await response.json()
          setCases(data)
          setError(null)
        } else {
          setError('Error al cargar casos')
        }
      } catch (err) {
        setError('Error de conexión')
      } finally {
        setIsLoading(false)
      }
    }

    fetchCases()
  }, [token, statusFilter])

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('es-CL', {
      day: 'numeric',
      month: 'short',
      year: 'numeric'
    })
  }

  const formatRelativeTime = (dateString: string) => {
    const date = new Date(dateString)
    const now = new Date()
    const diffMs = now.getTime() - date.getTime()
    const diffMins = Math.floor(diffMs / 60000)
    const diffHours = Math.floor(diffMins / 60)
    const diffDays = Math.floor(diffHours / 24)

    if (diffMins < 1) return 'Ahora'
    if (diffMins < 60) return `Hace ${diffMins} min`
    if (diffHours < 24) return `Hace ${diffHours}h`
    if (diffDays < 7) return `Hace ${diffDays} días`
    return formatDate(dateString)
  }

  return (
    <RoleGuard allowedRole="user">
      <PageHeader
        title="Mis Casos"
        description="Gestiona tus casos legales y comunicación con abogados"
      />

      {/* Filters */}
      <div className="flex flex-wrap gap-2 mb-6">
        <Button
          variant={statusFilter === null ? 'default' : 'outline'}
          size="sm"
          onClick={() => setStatusFilter(null)}
        >
          Todos
        </Button>
        <Button
          variant={statusFilter === 'in_progress' ? 'default' : 'outline'}
          size="sm"
          onClick={() => setStatusFilter('in_progress')}
        >
          En progreso
        </Button>
        <Button
          variant={statusFilter === 'transferred' ? 'default' : 'outline'}
          size="sm"
          onClick={() => setStatusFilter('transferred')}
        >
          Pendientes
        </Button>
        <Button
          variant={statusFilter === 'completed' ? 'default' : 'outline'}
          size="sm"
          onClick={() => setStatusFilter('completed')}
        >
          Completados
        </Button>
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="h-8 w-8 animate-spin text-pacific-500" />
        </div>
      ) : error ? (
        <div className="text-center py-12 text-red-600">{error}</div>
      ) : cases.length === 0 ? (
        <EmptyState
          icon={Briefcase}
          title="Sin casos"
          description="Aún no tienes casos registrados. Inicia una consulta con LEIA para crear tu primer caso."
          action={{
            label: 'Iniciar Consulta',
            href: '/chat'
          }}
        />
      ) : (
        <div className="space-y-4">
          {cases.map((caseItem) => {
            const status = statusConfig[caseItem.status] || statusConfig.draft
            const StatusIcon = status.icon
            const priority = priorityConfig[caseItem.priority] || priorityConfig.medium

            return (
              <Link
                key={caseItem.id}
                href={`/dashboard/usuario/caso/${caseItem.id}`}
                className="block"
              >
                <div className="glass-card rounded-xl p-4 hover:shadow-md transition-shadow cursor-pointer">
                  <div className="flex items-start justify-between">
                    <div className="flex-1 min-w-0">
                      {/* Header */}
                      <div className="flex items-center gap-2 mb-2">
                        <span className="text-sm font-mono text-slate-500">
                          {caseItem.case_number}
                        </span>
                        <span className={cn(
                          'px-2 py-0.5 rounded-full text-xs font-medium',
                          status.color
                        )}>
                          <StatusIcon className="h-3 w-3 inline mr-1" />
                          {status.label}
                        </span>
                        {caseItem.priority !== 'medium' && (
                          <span className={cn('text-xs font-medium', priority.color)}>
                            {priority.label}
                          </span>
                        )}
                      </div>

                      {/* Title */}
                      <h3 className="font-medium text-slate-900 mb-1 truncate">
                        {caseItem.title}
                      </h3>

                      {/* Summary */}
                      {caseItem.summary && (
                        <p className="text-sm text-slate-600 line-clamp-2 mb-2">
                          {caseItem.summary}
                        </p>
                      )}

                      {/* Meta */}
                      <div className="flex flex-wrap items-center gap-3 text-xs text-slate-500">
                        {caseItem.legal_area && (
                          <span className="bg-slate-100 px-2 py-0.5 rounded">
                            {caseItem.legal_area}
                          </span>
                        )}
                        {caseItem.region && (
                          <span>{caseItem.region}</span>
                        )}
                        <span>Creado {formatDate(caseItem.created_at)}</span>
                      </div>

                      {/* Last message preview */}
                      {caseItem.last_message && (
                        <div className="mt-3 p-2 bg-slate-50 rounded-lg">
                          <p className="text-sm text-slate-600 truncate">
                            <span className="font-medium">
                              {caseItem.last_message.sender_type === 'lawyer' ? 'Abogado: ' : 'Tú: '}
                            </span>
                            {caseItem.last_message.content}
                          </p>
                          <p className="text-xs text-slate-400 mt-1">
                            {formatRelativeTime(caseItem.last_message.created_at)}
                          </p>
                        </div>
                      )}
                    </div>

                    {/* Right side */}
                    <div className="flex flex-col items-end ml-4">
                      {caseItem.unread_messages > 0 && (
                        <div className="flex items-center gap-1 mb-2 px-2 py-1 bg-pacific-500 text-white rounded-full">
                          <MessageSquare className="h-3 w-3" />
                          <span className="text-xs font-medium">
                            {caseItem.unread_messages}
                          </span>
                        </div>
                      )}
                      <ArrowRight className="h-5 w-5 text-slate-400" />
                    </div>
                  </div>
                </div>
              </Link>
            )
          })}
        </div>
      )}

      {/* CTA */}
      <div className="mt-8 glass-card rounded-xl p-6 bg-gradient-to-br from-pacific-50 to-white">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
          <div>
            <h3 className="font-semibold text-slate-900">
              ¿Necesitas ayuda legal?
            </h3>
            <p className="text-sm text-slate-600">
              Inicia una consulta con LEIA para analizar tu situación
            </p>
          </div>
          <Button variant="pacific" asChild>
            <Link href="/chat">
              Nueva Consulta
              <ArrowRight className="h-4 w-4 ml-2" />
            </Link>
          </Button>
        </div>
      </div>
    </RoleGuard>
  )
}
