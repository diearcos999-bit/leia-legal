'use client'

import { useState, useEffect } from 'react'
import { useAuth } from '@/lib/auth'
import { RoleGuard, PageHeader, EmptyState, StatsCard } from '@/components/dashboard'
import {
  ClipboardList,
  Clock,
  CheckCircle,
  AlertTriangle,
  FileText,
  Loader2,
  Building2,
  Calendar
} from 'lucide-react'
import { cn } from '@/lib/utils'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface Tramite {
  id: number
  case_number: string
  tribunal: string
  tipo_tramite: string
  estado: string
  fecha_ingreso: string
  fecha_limite?: string
  cliente_nombre: string
  descripcion: string
}

const estadoConfig: Record<string, { label: string; color: string; icon: React.ElementType }> = {
  pendiente: { label: 'Pendiente', color: 'bg-yellow-100 text-yellow-700', icon: Clock },
  en_proceso: { label: 'En proceso', color: 'bg-pacific-100 text-pacific-700', icon: ClipboardList },
  completado: { label: 'Completado', color: 'bg-green-100 text-green-700', icon: CheckCircle },
  urgente: { label: 'Urgente', color: 'bg-red-100 text-red-700', icon: AlertTriangle }
}

export default function TramitesPage() {
  const { token } = useAuth()
  const [tramites, setTramites] = useState<Tramite[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // For now, use mock data - replace with API call when endpoint is ready
    const mockTramites: Tramite[] = [
      {
        id: 1,
        case_number: 'C-1234-2024',
        tribunal: '1er Juzgado Civil de Santiago',
        tipo_tramite: 'Notificacion personal',
        estado: 'pendiente',
        fecha_ingreso: '2024-01-15',
        fecha_limite: '2024-01-25',
        cliente_nombre: 'Maria Garcia',
        descripcion: 'Notificacion de demanda al demandado'
      },
      {
        id: 2,
        case_number: 'F-5678-2024',
        tribunal: 'Juzgado de Familia de Providencia',
        tipo_tramite: 'Retiro de documentos',
        estado: 'en_proceso',
        fecha_ingreso: '2024-01-10',
        cliente_nombre: 'Juan Rodriguez',
        descripcion: 'Retiro de sentencia ejecutoriada'
      },
      {
        id: 3,
        case_number: 'T-9012-2024',
        tribunal: '2do Juzgado del Trabajo de Santiago',
        tipo_tramite: 'Presentacion de escrito',
        estado: 'completado',
        fecha_ingreso: '2024-01-05',
        cliente_nombre: 'Ana Martinez',
        descripcion: 'Escrito de apelacion'
      }
    ]

    setTimeout(() => {
      setTramites(mockTramites)
      setIsLoading(false)
    }, 500)
  }, [token])

  const pendientes = tramites.filter(t => t.estado === 'pendiente').length
  const enProceso = tramites.filter(t => t.estado === 'en_proceso').length
  const completados = tramites.filter(t => t.estado === 'completado').length
  const urgentes = tramites.filter(t => t.estado === 'urgente').length

  return (
    <RoleGuard allowedRole="lawyer">
      <PageHeader
        title="Tramites Activos"
        description="Gestiona tus diligencias y tramites judiciales"
        icon={ClipboardList}
      />

      {/* Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatsCard
          title="Pendientes"
          value={pendientes}
          variant="warning"
          icon={Clock}
        />
        <StatsCard
          title="En proceso"
          value={enProceso}
          variant="pacific"
          icon={ClipboardList}
        />
        <StatsCard
          title="Completados"
          value={completados}
          variant="success"
          icon={CheckCircle}
        />
        <StatsCard
          title="Urgentes"
          value={urgentes}
          variant="terracota"
          icon={AlertTriangle}
        />
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="h-8 w-8 animate-spin text-pacific-500" />
        </div>
      ) : tramites.length === 0 ? (
        <EmptyState
          icon={ClipboardList}
          title="Sin tramites activos"
          description="Cuando tengas tramites asignados, apareceran aqui."
        />
      ) : (
        <div className="space-y-4">
          {tramites.map((tramite) => {
            const estado = estadoConfig[tramite.estado] || estadoConfig.pendiente
            const EstadoIcon = estado.icon

            return (
              <div
                key={tramite.id}
                className="glass-card rounded-xl p-4 hover:shadow-md transition-shadow"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    {/* Header */}
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-sm font-mono text-slate-500">
                        {tramite.case_number}
                      </span>
                      <span className={cn(
                        'px-2 py-0.5 rounded-full text-xs font-medium',
                        estado.color
                      )}>
                        <EstadoIcon className="h-3 w-3 inline mr-1" />
                        {estado.label}
                      </span>
                    </div>

                    {/* Tipo de tramite */}
                    <h3 className="font-medium text-slate-900 mb-2">
                      {tramite.tipo_tramite}
                    </h3>

                    {/* Description */}
                    <p className="text-sm text-slate-600 mb-3">
                      {tramite.descripcion}
                    </p>

                    {/* Meta */}
                    <div className="flex flex-wrap items-center gap-3 text-xs text-slate-500">
                      <span className="flex items-center gap-1">
                        <Building2 className="h-3 w-3" />
                        {tramite.tribunal}
                      </span>
                      <span className="flex items-center gap-1">
                        <FileText className="h-3 w-3" />
                        Cliente: {tramite.cliente_nombre}
                      </span>
                      {tramite.fecha_limite && (
                        <span className="flex items-center gap-1 text-orange-600">
                          <Calendar className="h-3 w-3" />
                          Limite: {new Date(tramite.fecha_limite).toLocaleDateString('es-CL')}
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      )}
    </RoleGuard>
  )
}
