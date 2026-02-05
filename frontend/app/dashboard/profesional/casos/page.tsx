'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { useAuth } from '@/lib/auth'
import { Button } from '@/components/ui/button'
import { RoleGuard, PageHeader, EmptyState, StatsCard } from '@/components/dashboard'
import {
  Briefcase,
  Filter,
  Clock,
  CheckCircle,
  XCircle,
  AlertCircle,
  Scale,
  ArrowRight,
  MessageSquare,
  Loader2,
  User
} from 'lucide-react'
import { cn } from '@/lib/utils'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface ActiveCase {
  transfer_id: number
  case_id: number
  case_number?: string
  case_title?: string
  case_status?: string
  legal_area?: string
  priority?: string
  user_name?: string
  accepted_at?: string
  unread_messages: number
  last_message?: {
    content: string
    sender_type: string
    created_at: string
  }
}

const statusConfig: Record<string, { label: string; color: string; icon: React.ElementType }> = {
  in_progress: { label: 'En progreso', color: 'bg-pacific-100 text-pacific-700', icon: Briefcase },
  completed: { label: 'Completado', color: 'bg-green-100 text-green-700', icon: CheckCircle },
  cancelled: { label: 'Cancelado', color: 'bg-red-100 text-red-700', icon: XCircle }
}

const priorityConfig: Record<string, { label: string; color: string }> = {
  low: { label: 'Baja', color: 'text-slate-500' },
  medium: { label: 'Media', color: 'text-yellow-600' },
  high: { label: 'Alta', color: 'text-orange-600' },
  urgent: { label: 'Urgente', color: 'text-red-600' }
}

export default function CasosPage() {
  const { token } = useAuth()
  const [cases, setCases] = useState<ActiveCase[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchCases = async () => {
      if (!token) return

      try {
        const response = await fetch(`${API_URL}/api/cases/lawyer/active`, {
          headers: { 'Authorization': `Bearer ${token}` }
        })

        if (response.ok) {
          const data = await response.json()
          setCases(data)
          setError(null)
        } else if (response.status === 403) {
          setError('Solo los abogados pueden ver casos')
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
  }, [token])

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

  // Calculate stats
  const activeCases = cases.filter(c => c.case_status === 'in_progress').length
  const completedCases = cases.filter(c => c.case_status === 'completed').length
  const totalUnread = cases.reduce((acc, c) => acc + c.unread_messages, 0)

  return (
    <RoleGuard allowedRole="lawyer">
      <PageHeader
        title="Gestión de Casos"
        description="Administra y da seguimiento a tus casos activos"
        icon={Briefcase}
        action={
          <Button variant="outline" asChild>
            <Link href="/dashboard/profesional/solicitudes">
              Ver solicitudes pendientes
            </Link>
          </Button>
        }
      />

      {/* Case Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatsCard
          title="Casos Activos"
          value={activeCases}
          variant="pacific"
          icon={Briefcase}
        />
        <StatsCard
          title="Mensajes sin leer"
          value={totalUnread}
          variant="warning"
          icon={MessageSquare}
        />
        <StatsCard
          title="Completados"
          value={completedCases}
          variant="success"
          icon={CheckCircle}
        />
        <StatsCard
          title="Total"
          value={cases.length}
          icon={Scale}
        />
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
          title="Sin casos activos"
          description="Cuando aceptes una solicitud de consulta, podrás gestionar el caso desde aquí."
          action={{
            label: 'Ver solicitudes',
            href: '/dashboard/profesional/solicitudes'
          }}
        />
      ) : (
        <div className="space-y-4">
          {cases.map((caseItem) => {
            const status = statusConfig[caseItem.case_status || 'in_progress'] || statusConfig.in_progress
            const StatusIcon = status.icon
            const priority = priorityConfig[caseItem.priority || 'medium']

            return (
              <Link
                key={caseItem.transfer_id}
                href={`/dashboard/profesional/caso/${caseItem.case_id}`}
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
                        {caseItem.priority && caseItem.priority !== 'medium' && (
                          <span className={cn('text-xs font-medium', priority.color)}>
                            {priority.label}
                          </span>
                        )}
                      </div>

                      {/* Title */}
                      <h3 className="font-medium text-slate-900 mb-2 truncate">
                        {caseItem.case_title}
                      </h3>

                      {/* Meta */}
                      <div className="flex flex-wrap items-center gap-3 text-xs text-slate-500">
                        {caseItem.legal_area && (
                          <span className="bg-slate-100 px-2 py-0.5 rounded">
                            {caseItem.legal_area}
                          </span>
                        )}
                        {caseItem.user_name && (
                          <span className="flex items-center gap-1">
                            <User className="h-3 w-3" />
                            {caseItem.user_name}
                          </span>
                        )}
                        {caseItem.accepted_at && (
                          <span>Aceptado {formatDate(caseItem.accepted_at)}</span>
                        )}
                      </div>

                      {/* Last message preview */}
                      {caseItem.last_message && (
                        <div className="mt-3 p-2 bg-slate-50 rounded-lg">
                          <p className="text-sm text-slate-600 truncate">
                            <span className="font-medium">
                              {caseItem.last_message.sender_type === 'user' ? 'Cliente: ' : 'Tú: '}
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
    </RoleGuard>
  )
}
