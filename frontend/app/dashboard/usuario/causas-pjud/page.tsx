'use client'

import { useState, useEffect } from 'react'
import { useAuth } from '@/lib/auth'
import { Button } from '@/components/ui/button'
import {
  Scale,
  RefreshCw,
  ChevronRight,
  Clock,
  FileText,
  AlertCircle,
  CheckCircle,
  Loader2,
  Eye,
  X,
  Calendar,
  Building,
  User,
  ArrowLeft
} from 'lucide-react'
import { cn } from '@/lib/utils'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface Actuacion {
  folio: string
  etapa: string
  tramite: string
  descripcion: string
  fecha: string
  foja: string
  tiene_documento: boolean
}

interface Causa {
  id: number
  tipo: string
  rit: string
  ruc: string
  tribunal: string
  caratulado: string
  fecha_ingreso: string
  estado: string
  procedimiento: string
  etapa: string
  ultima_actuacion: string | null
  fecha_ultima_actuacion: string | null
  actuaciones: Actuacion[]
  actuaciones_count: number
}

interface SyncStatus {
  has_data: boolean
  causas_count: number
  last_sync: string | null
  is_syncing: boolean
}

export default function CausasPJUDPage() {
  const { token } = useAuth()
  const [status, setStatus] = useState<SyncStatus | null>(null)
  const [causas, setCausas] = useState<Causa[]>([])
  const [selectedCausa, setSelectedCausa] = useState<Causa | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isSyncing, setIsSyncing] = useState(false)
  const [showSyncModal, setShowSyncModal] = useState(false)
  const [syncError, setSyncError] = useState<string | null>(null)
  const [credentials, setCredentials] = useState({ rut: '', password: '' })

  // Cargar estado inicial
  useEffect(() => {
    if (token) {
      loadStatus()
      loadCausas()
    }
  }, [token])

  const loadStatus = async () => {
    try {
      const res = await fetch(`${API_URL}/api/pjud/status`, {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      if (res.ok) {
        setStatus(await res.json())
      }
    } catch (e) {
      console.error('Error loading status:', e)
    }
  }

  const loadCausas = async () => {
    try {
      setIsLoading(true)
      const res = await fetch(`${API_URL}/api/pjud/causas`, {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      if (res.ok) {
        const data = await res.json()
        setCausas(data.causas || [])
      }
    } catch (e) {
      console.error('Error loading causas:', e)
    } finally {
      setIsLoading(false)
    }
  }

  const handleSync = async () => {
    if (!credentials.rut || !credentials.password) {
      setSyncError('Ingresa tu RUT y contraseña')
      return
    }

    setIsSyncing(true)
    setSyncError(null)

    try {
      const res = await fetch(`${API_URL}/api/pjud/sync`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          rut: credentials.rut.replace(/\./g, '').replace(/-/g, ''),
          password: credentials.password
        })
      })

      const data = await res.json()

      if (res.ok) {
        setShowSyncModal(false)
        setCredentials({ rut: '', password: '' })
        loadStatus()
        loadCausas()
      } else {
        setSyncError(data.detail || 'Error al sincronizar')
      }
    } catch (e) {
      setSyncError('Error de conexión')
    } finally {
      setIsSyncing(false)
    }
  }

  const getTipoColor = (tipo: string) => {
    const colors: Record<string, string> = {
      'Civil': 'bg-blue-100 text-blue-700',
      'Penal': 'bg-red-100 text-red-700',
      'Laboral': 'bg-green-100 text-green-700',
      'Familia': 'bg-purple-100 text-purple-700',
      'Cobranza': 'bg-yellow-100 text-yellow-700',
    }
    return colors[tipo] || 'bg-slate-100 text-slate-700'
  }

  const getEstadoColor = (estado: string) => {
    if (estado.toLowerCase().includes('conclu') || estado.toLowerCase().includes('fallad')) {
      return 'text-green-600'
    }
    if (estado.toLowerCase().includes('tramit')) {
      return 'text-blue-600'
    }
    return 'text-slate-600'
  }

  // Vista de detalle de causa
  if (selectedCausa) {
    return (
      <div className="p-6 max-w-5xl mx-auto">
        {/* Header */}
        <button
          onClick={() => setSelectedCausa(null)}
          className="flex items-center gap-2 text-slate-600 hover:text-slate-900 mb-6"
        >
          <ArrowLeft className="h-4 w-4" />
          Volver a mis causas
        </button>

        {/* Causa Header */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 mb-6">
          <div className="flex items-start justify-between mb-4">
            <div>
              <span className={cn("px-3 py-1 rounded-full text-sm font-medium", getTipoColor(selectedCausa.tipo))}>
                {selectedCausa.tipo}
              </span>
              <h1 className="text-2xl font-bold text-slate-900 mt-2">{selectedCausa.rit}</h1>
              <p className="text-lg text-slate-600">{selectedCausa.caratulado}</p>
            </div>
            <span className={cn("text-sm font-medium", getEstadoColor(selectedCausa.estado))}>
              {selectedCausa.estado}
            </span>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div>
              <p className="text-slate-500">Tribunal</p>
              <p className="font-medium text-slate-900">{selectedCausa.tribunal}</p>
            </div>
            {selectedCausa.ruc && (
              <div>
                <p className="text-slate-500">RUC</p>
                <p className="font-medium text-slate-900">{selectedCausa.ruc}</p>
              </div>
            )}
            <div>
              <p className="text-slate-500">Fecha Ingreso</p>
              <p className="font-medium text-slate-900">{selectedCausa.fecha_ingreso}</p>
            </div>
            {selectedCausa.procedimiento && (
              <div>
                <p className="text-slate-500">Procedimiento</p>
                <p className="font-medium text-slate-900">{selectedCausa.procedimiento}</p>
              </div>
            )}
          </div>
        </div>

        {/* Última actuación */}
        {selectedCausa.ultima_actuacion && (
          <div className="bg-pacific-50 border border-pacific-200 rounded-xl p-4 mb-6">
            <div className="flex items-center gap-2 mb-2">
              <Clock className="h-4 w-4 text-pacific-600" />
              <span className="text-sm font-medium text-pacific-700">Última actuación</span>
            </div>
            <p className="text-slate-900 font-medium">{selectedCausa.ultima_actuacion}</p>
            <p className="text-sm text-slate-600">{selectedCausa.fecha_ultima_actuacion}</p>
          </div>
        )}

        {/* Historial de actuaciones */}
        <div className="bg-white rounded-2xl border border-slate-200">
          <div className="p-4 border-b border-slate-200">
            <h2 className="text-lg font-semibold text-slate-900">
              Historial de Actuaciones ({selectedCausa.actuaciones.length})
            </h2>
          </div>

          {selectedCausa.actuaciones.length === 0 ? (
            <div className="p-8 text-center text-slate-500">
              No hay actuaciones registradas
            </div>
          ) : (
            <div className="divide-y divide-slate-100 max-h-[600px] overflow-y-auto">
              {selectedCausa.actuaciones.map((act, idx) => (
                <div key={idx} className="p-4 hover:bg-slate-50 transition-colors">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-1">
                        <span className="text-sm font-mono text-slate-500">#{act.folio}</span>
                        {act.etapa && (
                          <span className="text-xs px-2 py-0.5 bg-slate-100 text-slate-600 rounded">
                            {act.etapa}
                          </span>
                        )}
                        {act.tramite && (
                          <span className="text-xs text-slate-500">{act.tramite}</span>
                        )}
                      </div>
                      <p className="text-slate-900 font-medium">{act.descripcion}</p>
                    </div>
                    <div className="text-right ml-4">
                      <p className="text-sm text-slate-600">{act.fecha}</p>
                      {act.foja && act.foja !== '0' && (
                        <p className="text-xs text-slate-400">Foja {act.foja}</p>
                      )}
                      {act.tiene_documento && (
                        <FileText className="h-4 w-4 text-pacific-500 ml-auto mt-1" />
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    )
  }

  // Vista principal - Lista de causas
  return (
    <div className="p-6 max-w-5xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Mis Causas - Poder Judicial</h1>
          <p className="text-slate-600">Sincroniza con tu ClaveÚnica y consulta tus causas judiciales</p>
        </div>
        <Button
          onClick={() => setShowSyncModal(true)}
          variant="pacific"
          disabled={isSyncing}
        >
          {isSyncing ? (
            <Loader2 className="h-4 w-4 animate-spin mr-2" />
          ) : (
            <RefreshCw className="h-4 w-4 mr-2" />
          )}
          Sincronizar
        </Button>
      </div>

      {/* Status */}
      {status?.last_sync && (
        <div className="bg-slate-50 rounded-lg px-4 py-2 mb-6 flex items-center gap-2 text-sm text-slate-600">
          <CheckCircle className="h-4 w-4 text-green-500" />
          Última sincronización: {new Date(status.last_sync).toLocaleString('es-CL')}
          <span className="text-slate-400">•</span>
          {status.causas_count} causas
        </div>
      )}

      {/* Loading */}
      {isLoading ? (
        <div className="flex items-center justify-center py-20">
          <Loader2 className="h-8 w-8 animate-spin text-pacific-500" />
        </div>
      ) : causas.length === 0 ? (
        /* Empty state */
        <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center">
          <Scale className="h-16 w-16 text-slate-300 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-slate-900 mb-2">
            No hay causas sincronizadas
          </h2>
          <p className="text-slate-600 mb-2 max-w-md mx-auto">
            Sincroniza tus causas desde la Oficina Judicial Virtual para ver
            el estado de tus procesos judiciales.
          </p>
          <p className="text-slate-500 text-sm mb-6 max-w-md mx-auto">
            Solo necesitas tu <span className="font-semibold text-pacific-600">ClaveÚnica</span> del Estado de Chile.
          </p>
          <Button onClick={() => setShowSyncModal(true)} variant="pacific">
            <RefreshCw className="h-4 w-4 mr-2" />
            Sincronizar ahora
          </Button>
        </div>
      ) : (
        /* Lista de causas */
        <div className="space-y-4">
          {causas.map((causa) => (
            <div
              key={causa.id}
              onClick={() => setSelectedCausa(causa)}
              className="bg-white rounded-xl border border-slate-200 p-5 hover:border-pacific-300 hover:shadow-md transition-all cursor-pointer"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <span className={cn("px-2 py-0.5 rounded text-xs font-medium", getTipoColor(causa.tipo))}>
                      {causa.tipo}
                    </span>
                    <span className="text-lg font-semibold text-slate-900">{causa.rit}</span>
                  </div>
                  <p className="text-slate-700 font-medium mb-1">{causa.caratulado}</p>
                  <p className="text-sm text-slate-500 flex items-center gap-1">
                    <Building className="h-3 w-3" />
                    {causa.tribunal}
                  </p>
                </div>

                <div className="text-right">
                  <span className={cn("text-sm font-medium", getEstadoColor(causa.estado))}>
                    {causa.estado}
                  </span>
                  <p className="text-xs text-slate-400 mt-1">{causa.fecha_ingreso}</p>
                </div>
              </div>

              {causa.ultima_actuacion && (
                <div className="mt-3 pt-3 border-t border-slate-100">
                  <div className="flex items-center justify-between text-sm">
                    <div className="flex items-center gap-2 text-slate-600">
                      <Clock className="h-3 w-3" />
                      <span>{causa.ultima_actuacion}</span>
                    </div>
                    <span className="text-slate-400">{causa.fecha_ultima_actuacion}</span>
                  </div>
                </div>
              )}

              <div className="mt-3 flex items-center justify-between">
                <span className="text-xs text-slate-400">
                  {causa.actuaciones_count} actuaciones
                </span>
                <span className="text-pacific-600 text-sm flex items-center gap-1">
                  Ver detalle <ChevronRight className="h-4 w-4" />
                </span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modal de sincronización */}
      {showSyncModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl max-w-md w-full p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-slate-900">Sincronizar Causas</h2>
              <button onClick={() => setShowSyncModal(false)} className="text-slate-400 hover:text-slate-600">
                <X className="h-5 w-5" />
              </button>
            </div>

            <div className="bg-pacific-50 border border-pacific-200 rounded-lg p-4 mb-6">
              <p className="text-pacific-900 text-sm font-medium mb-1">
                Usa tu ClaveÚnica del Estado de Chile
              </p>
              <p className="text-pacific-700 text-xs">
                Es la misma clave que usas para el SII, Registro Civil, Fonasa y otros servicios del Estado.
              </p>
            </div>

            {syncError && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-3 mb-4 flex items-center gap-2 text-red-700 text-sm">
                <AlertCircle className="h-4 w-4" />
                {syncError}
              </div>
            )}

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">RUT</label>
                <input
                  type="text"
                  value={credentials.rut}
                  onChange={(e) => setCredentials(prev => ({ ...prev, rut: e.target.value }))}
                  placeholder="12.345.678-9"
                  className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-pacific-500 focus:border-pacific-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Contraseña</label>
                <input
                  type="password"
                  value={credentials.password}
                  onChange={(e) => setCredentials(prev => ({ ...prev, password: e.target.value }))}
                  placeholder="Tu contraseña de ClaveÚnica"
                  className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-pacific-500 focus:border-pacific-500"
                />
              </div>
            </div>

            <div className="flex gap-3 mt-6">
              <Button
                variant="outline"
                className="flex-1"
                onClick={() => setShowSyncModal(false)}
                disabled={isSyncing}
              >
                Cancelar
              </Button>
              <Button
                variant="pacific"
                className="flex-1"
                onClick={handleSync}
                disabled={isSyncing}
              >
                {isSyncing ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin mr-2" />
                    Sincronizando...
                  </>
                ) : (
                  'Sincronizar'
                )}
              </Button>
            </div>

            <p className="text-xs text-slate-400 mt-4 text-center">
              🔒 Conexión segura con ClaveÚnica. Tus credenciales no se almacenan.
            </p>
          </div>
        </div>
      )}
    </div>
  )
}
