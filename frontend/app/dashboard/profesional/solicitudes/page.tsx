'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { useAuth } from '@/lib/auth'
import { Button } from '@/components/ui/button'
import { RoleGuard, PageHeader, EmptyState } from '@/components/dashboard'
import {
  Inbox,
  Clock,
  CheckCircle,
  XCircle,
  Scale,
  MapPin,
  Calendar,
  ArrowRight,
  Loader2,
  AlertTriangle,
  User
} from 'lucide-react'
import { cn } from '@/lib/utils'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface PendingTransfer {
  transfer_id: number
  case_id: number
  case_number?: string
  case_title?: string
  case_summary?: string
  legal_area?: string
  priority?: string
  user_name?: string
  user_message?: string
  service_type?: string
  created_at: string
}

const priorityConfig: Record<string, { label: string; color: string }> = {
  low: { label: 'Baja', color: 'text-slate-500 bg-slate-100' },
  medium: { label: 'Media', color: 'text-yellow-700 bg-yellow-100' },
  high: { label: 'Alta', color: 'text-orange-700 bg-orange-100' },
  urgent: { label: 'Urgente', color: 'text-red-700 bg-red-100' }
}

export default function SolicitudesPage() {
  const { token } = useAuth()
  const [transfers, setTransfers] = useState<PendingTransfer[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [processingId, setProcessingId] = useState<number | null>(null)
  const [showRejectModal, setShowRejectModal] = useState<number | null>(null)
  const [rejectReason, setRejectReason] = useState('')

  const fetchTransfers = async () => {
    if (!token) return

    try {
      const response = await fetch(`${API_URL}/api/cases/lawyer/pending`, {
        headers: { 'Authorization': `Bearer ${token}` }
      })

      if (response.ok) {
        const data = await response.json()
        setTransfers(data)
        setError(null)
      } else if (response.status === 403) {
        setError('Solo los abogados pueden ver solicitudes')
      } else {
        setError('Error al cargar solicitudes')
      }
    } catch (err) {
      setError('Error de conexión')
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchTransfers()
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
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60))
    const diffDays = Math.floor(diffHours / 24)

    if (diffHours < 1) return 'Hace menos de 1 hora'
    if (diffHours < 24) return `Hace ${diffHours} horas`
    if (diffDays === 1) return 'Ayer'
    if (diffDays < 7) return `Hace ${diffDays} días`
    return formatDate(dateString)
  }

  const handleAccept = async (transferId: number) => {
    if (!token) return

    setProcessingId(transferId)

    try {
      const response = await fetch(`${API_URL}/api/cases/transfers/${transferId}/accept`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          response: 'Acepto revisar tu caso. Me pondré en contacto contigo pronto.',
          agreed_price: null
        })
      })

      if (response.ok) {
        // Remove from list
        setTransfers(prev => prev.filter(t => t.transfer_id !== transferId))
      } else {
        const data = await response.json()
        setError(data.detail || 'Error al aceptar solicitud')
      }
    } catch (err) {
      setError('Error de conexión')
    } finally {
      setProcessingId(null)
    }
  }

  const handleReject = async (transferId: number) => {
    if (!token) return

    setProcessingId(transferId)

    try {
      const response = await fetch(`${API_URL}/api/cases/transfers/${transferId}/reject`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          response: rejectReason || 'No puedo aceptar este caso en este momento.'
        })
      })

      if (response.ok) {
        setTransfers(prev => prev.filter(t => t.transfer_id !== transferId))
        setShowRejectModal(null)
        setRejectReason('')
      } else {
        const data = await response.json()
        setError(data.detail || 'Error al rechazar solicitud')
      }
    } catch (err) {
      setError('Error de conexión')
    } finally {
      setProcessingId(null)
    }
  }

  return (
    <RoleGuard allowedRole="lawyer">
      <PageHeader
        title="Solicitudes"
        description="Solicitudes de consulta de clientes pendientes de respuesta"
        icon={Inbox}
      />

      {isLoading ? (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="h-8 w-8 animate-spin text-pacific-500" />
        </div>
      ) : error ? (
        <div className="text-center py-12">
          <AlertTriangle className="h-12 w-12 mx-auto text-red-500 mb-4" />
          <p className="text-red-600">{error}</p>
        </div>
      ) : transfers.length === 0 ? (
        <EmptyState
          icon={Inbox}
          title="Sin solicitudes nuevas"
          description="Cuando un cliente solicite tu servicio, verás la solicitud aquí. Completa tu perfil para recibir más consultas."
          action={{
            label: 'Completar Perfil',
            href: '/dashboard/profesional/perfil-publico'
          }}
        />
      ) : (
        <div className="space-y-4">
          {transfers.map((transfer) => {
            const priority = priorityConfig[transfer.priority || 'medium']

            return (
              <div key={transfer.transfer_id} className="glass-card rounded-xl p-6">
                <div className="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-4">
                  {/* Main info */}
                  <div className="flex-1">
                    {/* Header */}
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-sm font-mono text-slate-500">
                        {transfer.case_number}
                      </span>
                      {transfer.priority && transfer.priority !== 'medium' && (
                        <span className={cn(
                          'px-2 py-0.5 rounded-full text-xs font-medium',
                          priority.color
                        )}>
                          {priority.label}
                        </span>
                      )}
                      <span className="text-xs text-slate-400">
                        {formatRelativeTime(transfer.created_at)}
                      </span>
                    </div>

                    {/* Title */}
                    <h3 className="font-semibold text-slate-900 mb-2">
                      {transfer.case_title}
                    </h3>

                    {/* Summary */}
                    {transfer.case_summary && (
                      <p className="text-sm text-slate-600 mb-3 line-clamp-2">
                        {transfer.case_summary}
                      </p>
                    )}

                    {/* Meta */}
                    <div className="flex flex-wrap items-center gap-3 text-xs text-slate-500 mb-4">
                      {transfer.legal_area && (
                        <span className="flex items-center gap-1 bg-slate-100 px-2 py-1 rounded">
                          <Scale className="h-3 w-3" />
                          {transfer.legal_area}
                        </span>
                      )}
                      {transfer.user_name && (
                        <span className="flex items-center gap-1">
                          <User className="h-3 w-3" />
                          {transfer.user_name}
                        </span>
                      )}
                      {transfer.service_type && (
                        <span className="bg-pacific-100 text-pacific-700 px-2 py-1 rounded">
                          {transfer.service_type}
                        </span>
                      )}
                    </div>

                    {/* User message */}
                    {transfer.user_message && (
                      <div className="p-3 bg-slate-50 rounded-lg">
                        <p className="text-xs text-slate-500 mb-1">Mensaje del cliente:</p>
                        <p className="text-sm text-slate-700">{transfer.user_message}</p>
                      </div>
                    )}
                  </div>

                  {/* Actions */}
                  <div className="flex flex-col gap-2 lg:ml-4">
                    <Link href={`/dashboard/profesional/caso/${transfer.case_id}`}>
                      <Button variant="outline" size="sm" className="w-full">
                        Ver detalles
                        <ArrowRight className="h-4 w-4 ml-1" />
                      </Button>
                    </Link>
                    <Button
                      variant="pacific"
                      size="sm"
                      onClick={() => handleAccept(transfer.transfer_id)}
                      disabled={processingId === transfer.transfer_id}
                      className="w-full"
                    >
                      {processingId === transfer.transfer_id ? (
                        <Loader2 className="h-4 w-4 animate-spin" />
                      ) : (
                        <>
                          <CheckCircle className="h-4 w-4 mr-1" />
                          Aceptar
                        </>
                      )}
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setShowRejectModal(transfer.transfer_id)}
                      disabled={processingId === transfer.transfer_id}
                      className="w-full text-red-600 hover:text-red-700 hover:bg-red-50"
                    >
                      <XCircle className="h-4 w-4 mr-1" />
                      Rechazar
                    </Button>
                  </div>
                </div>

                {/* Reject modal */}
                {showRejectModal === transfer.transfer_id && (
                  <div className="mt-4 pt-4 border-t border-slate-200">
                    <p className="text-sm font-medium text-slate-700 mb-2">
                      Motivo del rechazo (opcional):
                    </p>
                    <textarea
                      value={rejectReason}
                      onChange={(e) => setRejectReason(e.target.value)}
                      className="w-full p-3 text-sm border border-slate-200 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-pacific-500"
                      rows={2}
                      placeholder="Ej: No tengo disponibilidad en este momento..."
                    />
                    <div className="flex gap-2 mt-3">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => {
                          setShowRejectModal(null)
                          setRejectReason('')
                        }}
                      >
                        Cancelar
                      </Button>
                      <Button
                        variant="destructive"
                        size="sm"
                        onClick={() => handleReject(transfer.transfer_id)}
                        disabled={processingId === transfer.transfer_id}
                      >
                        {processingId === transfer.transfer_id ? (
                          <Loader2 className="h-4 w-4 animate-spin" />
                        ) : (
                          'Confirmar rechazo'
                        )}
                      </Button>
                    </div>
                  </div>
                )}
              </div>
            )
          })}
        </div>
      )}
    </RoleGuard>
  )
}
