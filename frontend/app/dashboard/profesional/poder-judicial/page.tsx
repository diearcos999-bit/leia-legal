'use client'

import { useState, useEffect, useCallback } from 'react'
import {
  Building2,
  Shield,
  RefreshCw,
  CheckCircle2,
  Clock,
  FileText,
  ExternalLink,
  AlertCircle,
  X,
  Loader2,
  AlertTriangle,
  KeyRound,
  Eye,
  EyeOff
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { RoleGuard, PageHeader, StatsCard } from '@/components/dashboard'
import { LeiaAvatar } from '@/components/ui/leia-avatar'
import { cn } from '@/lib/utils'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface Causa {
  id: number
  rit: string
  tribunal: string | null
  caratulado: string | null
  materia: string | null
  estado: string | null
  fecha_ingreso: string | null
  ultima_actuacion: string | null
  fecha_actuacion: string | null
  proxima_audiencia: string | null
}

interface ConnectionStatus {
  has_data: boolean
  causas_count: number
  last_sync: string | null
  is_syncing: boolean
}

type ConnectionState = 'disconnected' | 'connecting' | 'connected' | 'syncing' | 'error'

// Info sobre ClaveÚnica
const claveUnicaInfo = {
  title: "¿Qué es ClaveÚnica?",
  description: "Es la contraseña única del Estado de Chile que te permite acceder a todos los servicios públicos digitales, incluyendo el Poder Judicial.",
  examples: "Es la misma clave que usas para el SII, Registro Civil, Fonasa y otros servicios del Estado.",
  tip: "Si ya tienes ClaveÚnica, puedes conectarte inmediatamente."
}

export default function PoderJudicialPage() {
  const [connectionState, setConnectionState] = useState<ConnectionState>('disconnected')
  const [showLoginModal, setShowLoginModal] = useState(false)
  const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus | null>(null)
  const [causas, setCausas] = useState<Causa[]>([])
  const [error, setError] = useState<string | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [showPassword, setShowPassword] = useState(false)

  // Form state
  const [rut, setRut] = useState('')
  const [password, setPassword] = useState('')

  const getAuthHeader = (): Record<string, string> => {
    const token = localStorage.getItem('justiciaai_token')
    return token ? { Authorization: `Bearer ${token}` } : {}
  }

  const fetchConnectionStatus = useCallback(async () => {
    try {
      const response = await fetch(`${API_URL}/api/pjud/status`, {
        headers: getAuthHeader()
      })

      if (response.ok) {
        const data: ConnectionStatus = await response.json()
        setConnectionStatus(data)

        if (data.is_syncing) {
          setConnectionState('syncing')
        } else if (data.has_data) {
          setConnectionState('connected')
        } else {
          setConnectionState('disconnected')
        }
      }
    } catch (err) {
      console.error('Error fetching status:', err)
    }
  }, [])

  const fetchCausas = useCallback(async () => {
    try {
      const response = await fetch(`${API_URL}/api/pjud/causas`, {
        headers: getAuthHeader()
      })

      if (response.ok) {
        const data = await response.json()
        setCausas(data.causas || [])
      }
    } catch (err) {
      console.error('Error fetching causas:', err)
    }
  }, [])

  useEffect(() => {
    fetchConnectionStatus()
  }, [fetchConnectionStatus])

  useEffect(() => {
    if (connectionState === 'connected') {
      fetchCausas()
    }
  }, [connectionState, fetchCausas])

  // Poll for sync status while syncing
  useEffect(() => {
    if (connectionState === 'syncing') {
      const interval = setInterval(() => {
        fetchConnectionStatus()
        fetchCausas()
      }, 3000)
      return () => clearInterval(interval)
    }
  }, [connectionState, fetchConnectionStatus, fetchCausas])

  const formatRut = (value: string) => {
    const cleaned = value.replace(/[^0-9kK]/g, '').toUpperCase()
    if (cleaned.length <= 1) return cleaned
    const rutBody = cleaned.slice(0, -1)
    const dv = cleaned.slice(-1)
    let formatted = ''
    for (let i = rutBody.length - 1, j = 0; i >= 0; i--, j++) {
      if (j > 0 && j % 3 === 0) formatted = '.' + formatted
      formatted = rutBody[i] + formatted
    }
    return `${formatted}-${dv}`
  }

  const handleRutChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setRut(formatRut(e.target.value))
  }

  const handleConnect = () => {
    setShowLoginModal(true)
    setError(null)
  }

  const handleSubmitLogin = async () => {
    if (!rut || !password) {
      setError('Ingresa tu RUT y contraseña')
      return
    }

    setIsSubmitting(true)
    setError(null)
    setShowLoginModal(false)
    setConnectionState('syncing')

    try {
      // Limpiar RUT (quitar puntos y guión)
      const rutClean = rut.replace(/\./g, '').replace(/-/g, '')

      const response = await fetch(`${API_URL}/api/pjud/sync`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeader()
        },
        body: JSON.stringify({ rut: rutClean, password })
      })

      const data = await response.json()

      if (response.ok) {
        setConnectionState('connected')
        setRut('')
        setPassword('')
        fetchConnectionStatus()
        fetchCausas()
      } else {
        setError(data.detail || 'Error al sincronizar')
        setConnectionState('error')
      }
    } catch (err) {
      setError('Error de conexión. Intenta nuevamente.')
      setConnectionState('error')
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleRefresh = () => {
    // Para actualizar, el usuario debe volver a ingresar sus credenciales
    setShowLoginModal(true)
    setError(null)
  }

  const handleDisconnect = async () => {
    try {
      const response = await fetch(`${API_URL}/api/pjud/clear`, {
        method: 'DELETE',
        headers: getAuthHeader()
      })

      if (response.ok) {
        setConnectionState('disconnected')
        setConnectionStatus(null)
        setCausas([])
      }
    } catch (err) {
      console.error('Error disconnecting:', err)
    }
  }

  return (
    <RoleGuard allowedRole="lawyer">
      <PageHeader
        title="Poder Judicial"
        description="Conexión con el sistema judicial chileno"
        icon={Building2}
        action={
          connectionState === 'connected' && (
            <div className="flex items-center gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={handleRefresh}
              >
                <RefreshCw className="h-4 w-4 mr-2" />
                Actualizar Causas
              </Button>
            </div>
          )
        }
      />

      {/* Disconnected State */}
      {connectionState === 'disconnected' && (
        <div className="max-w-2xl mx-auto">
          <div className="glass-card rounded-2xl p-8 text-center">
            {/* LEIA Avatar */}
            <div className="flex justify-center mb-2">
              <LeiaAvatar size="sm" animated={true} />
            </div>

            <h2 className="text-2xl font-semibold text-slate-900 mb-3">
              Conecta con el Poder Judicial
            </h2>
            <p className="text-slate-600 mb-2 max-w-md mx-auto">
              Sincroniza tus causas desde la Oficina Judicial Virtual para ver y dar seguimiento a todos tus procesos judiciales desde LEIA.
            </p>
            <p className="text-slate-500 text-sm mb-4 max-w-md mx-auto">
              Solo necesitas tu <span className="font-semibold text-pacific-600">ClaveÚnica</span> del Estado de Chile.
            </p>

            {/* Action Button */}
            <div className="flex flex-col sm:flex-row gap-3 justify-center mb-8">
              <Button
                variant="pacific"
                size="lg"
                onClick={handleConnect}
              >
                <KeyRound className="h-5 w-5 mr-2" />
                Conectar con ClaveÚnica
              </Button>
            </div>

            {/* Benefits */}
            <div className="grid sm:grid-cols-3 gap-4 text-left">
              <div className="p-4 rounded-xl bg-white/50">
                <div className="w-10 h-10 rounded-lg bg-pacific-100 flex items-center justify-center mb-3">
                  <RefreshCw className="h-5 w-5 text-pacific-600" />
                </div>
                <h3 className="font-medium text-slate-900 mb-1">Sincronización</h3>
                <p className="text-sm text-slate-500">
                  Actualización automática del estado de tus causas
                </p>
              </div>
              <div className="p-4 rounded-xl bg-white/50">
                <div className="w-10 h-10 rounded-lg bg-pacific-100 flex items-center justify-center mb-3">
                  <AlertCircle className="h-5 w-5 text-pacific-600" />
                </div>
                <h3 className="font-medium text-slate-900 mb-1">Notificaciones</h3>
                <p className="text-sm text-slate-500">
                  Alertas de nuevas actuaciones y audiencias
                </p>
              </div>
              <div className="p-4 rounded-xl bg-white/50">
                <div className="w-10 h-10 rounded-lg bg-pacific-100 flex items-center justify-center mb-3">
                  <Shield className="h-5 w-5 text-pacific-600" />
                </div>
                <h3 className="font-medium text-slate-900 mb-1">Seguro</h3>
                <p className="text-sm text-slate-500">
                  Conexión segura con ClaveÚnica del Estado
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Syncing State */}
      {connectionState === 'syncing' && (
        <div className="max-w-2xl mx-auto">
          <div className="glass-card rounded-2xl p-8 text-center">
            {/* Animated LEIA */}
            <div className="flex justify-center mb-4">
              <LeiaAvatar size="sm" animated={true} />
            </div>

            <h2 className="text-2xl font-semibold text-slate-900 mb-3">
              Sincronizando tus causas...
            </h2>
            <p className="text-slate-600 mb-6">
              Estoy conectándome al Poder Judicial para extraer la información de tus causas.
              Esto tomará solo unos segundos.
            </p>

            <div className="flex items-center justify-center gap-2 text-sm text-pacific-600 font-medium">
              <Loader2 className="h-4 w-4 animate-spin" />
              Procesando...
            </div>
          </div>
        </div>
      )}

      {/* Error State */}
      {connectionState === 'error' && (
        <div className="max-w-2xl mx-auto">
          <div className="glass-card rounded-2xl p-8 text-center">
            <div className="w-20 h-20 rounded-2xl bg-red-100 flex items-center justify-center mx-auto mb-6">
              <AlertTriangle className="h-10 w-10 text-red-600" />
            </div>

            <h2 className="text-2xl font-semibold text-slate-900 mb-3">
              Error de sincronización
            </h2>
            <p className="text-slate-600 mb-6">
              No pudimos sincronizar tus causas. Esto puede deberse a credenciales incorrectas
              o problemas con el servicio del Poder Judicial.
            </p>

            <div className="flex gap-3 justify-center">
              <Button variant="outline" onClick={handleDisconnect}>
                Desconectar
              </Button>
              <Button variant="pacific" onClick={handleConnect}>
                Reintentar conexión
              </Button>
            </div>
          </div>
        </div>
      )}

      {/* Connected State */}
      {connectionState === 'connected' && (
        <>
          {/* Connection Status Bar */}
          <div className="glass-card rounded-2xl p-4 mb-6 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center">
                <CheckCircle2 className="h-5 w-5 text-green-600" />
              </div>
              <div>
                <p className="font-medium text-slate-900">
                  Conectado - {connectionStatus?.causas_count || 0} causas sincronizadas
                </p>
                <p className="text-sm text-slate-500">
                  Última sincronización: {connectionStatus?.last_sync
                    ? new Date(connectionStatus.last_sync).toLocaleString('es-CL')
                    : 'Nunca'}
                </p>
              </div>
            </div>
            <Button variant="ghost" size="sm" onClick={handleDisconnect} className="text-slate-500">
              Desconectar
            </Button>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            <StatsCard
              title="Causas Activas"
              value={causas.filter(c => c.estado?.toLowerCase().includes('tramitación')).length}
              icon={FileText}
              variant="pacific"
            />
            <StatsCard
              title="Con Sentencia"
              value={causas.filter(c => c.estado?.toLowerCase().includes('sentencia')).length}
              icon={CheckCircle2}
              variant="success"
            />
            <StatsCard
              title="Próximas Audiencias"
              value={causas.filter(c => c.proxima_audiencia).length}
              icon={Clock}
              variant="warning"
            />
            <StatsCard
              title="Total Causas"
              value={causas.length}
              icon={Building2}
            />
          </div>

          {/* Causas List */}
          <div className="glass-card rounded-2xl p-6">
            <h2 className="text-lg font-semibold text-slate-900 mb-4">
              Mis Causas
            </h2>

            {causas.length === 0 ? (
              <div className="text-center py-8">
                <FileText className="h-12 w-12 text-slate-300 mx-auto mb-3" />
                <p className="text-slate-500">No se encontraron causas asociadas a tu RUT</p>
              </div>
            ) : (
              <div className="space-y-4">
                {causas.map((causa) => (
                  <div
                    key={causa.id}
                    className="p-4 rounded-xl bg-white/50 border border-white/40 hover:bg-white/70 transition-colors"
                  >
                    <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="font-semibold text-slate-900">{causa.rit}</span>
                          {causa.estado && (
                            <span className={cn(
                              "px-2 py-0.5 text-xs font-medium rounded-full",
                              causa.estado.toLowerCase().includes('tramitación')
                                ? "bg-amber-100 text-amber-700"
                                : "bg-green-100 text-green-700"
                            )}>
                              {causa.estado}
                            </span>
                          )}
                        </div>
                        <p className="text-sm text-slate-600 mb-1">{causa.caratulado || 'Sin carátula'}</p>
                        <p className="text-xs text-slate-500">{causa.tribunal || 'Tribunal no especificado'}</p>
                      </div>

                      <div className="flex flex-col sm:flex-row gap-4 lg:text-right">
                        {causa.ultima_actuacion && (
                          <div>
                            <p className="text-xs text-slate-500">Última actuación</p>
                            <p className="text-sm font-medium text-slate-700">{causa.ultima_actuacion}</p>
                            {causa.fecha_actuacion && (
                              <p className="text-xs text-slate-400">{causa.fecha_actuacion}</p>
                            )}
                          </div>
                        )}
                        {causa.proxima_audiencia && (
                          <div className="sm:border-l sm:pl-4 border-slate-200">
                            <p className="text-xs text-slate-500">Próxima audiencia</p>
                            <p className="text-sm font-medium text-pacific-600">{causa.proxima_audiencia}</p>
                          </div>
                        )}
                      </div>

                      <Button
                        variant="ghost"
                        size="sm"
                        className="lg:ml-4"
                        onClick={() => window.open(`https://oficinajudicialvirtual.pjud.cl`, '_blank')}
                      >
                        <ExternalLink className="h-4 w-4 mr-1" />
                        Ver en PJUD
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </>
      )}


      {/* Login Modal - Ingresar credenciales */}
      {showLoginModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div
            className="absolute inset-0 bg-black/30 backdrop-blur-sm"
            onClick={() => !isSubmitting && setShowLoginModal(false)}
          />
          <div className="relative glass-panel rounded-2xl p-6 max-w-md w-full animate-scale-in">
            {!isSubmitting && (
              <button
                onClick={() => setShowLoginModal(false)}
                className="absolute top-4 right-4 p-1 rounded-lg hover:bg-slate-100 transition-colors"
              >
                <X className="h-5 w-5 text-slate-500" />
              </button>
            )}

            <div className="text-center mb-6">
              <div className="w-16 h-16 rounded-2xl bg-pacific-100 flex items-center justify-center mx-auto mb-4">
                <KeyRound className="h-8 w-8 text-pacific-600" />
              </div>
              <h3 className="text-lg font-semibold text-slate-900 mb-2">
                Conectar con ClaveÚnica
              </h3>
              <p className="text-sm text-slate-500">
                Usa tu ClaveÚnica del Estado de Chile para sincronizar tus causas
              </p>
            </div>

            {error && (
              <div className="mb-4 p-3 rounded-xl bg-red-50 border border-red-200 text-sm text-red-600 flex items-center gap-2">
                <AlertCircle className="h-4 w-4 flex-shrink-0" />
                {error}
              </div>
            )}

            <div className="space-y-4 mb-6">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  RUT
                </label>
                <input
                  type="text"
                  value={rut}
                  onChange={handleRutChange}
                  placeholder="12.345.678-9"
                  className="w-full px-4 py-2.5 rounded-xl bg-white/50 border border-slate-200 text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-pacific-500/20 focus:border-pacific-500"
                  disabled={isSubmitting}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  Contraseña
                </label>
                <div className="relative">
                  <input
                    type={showPassword ? "text" : "password"}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Tu contraseña de ClaveÚnica"
                    className="w-full px-4 py-2.5 pr-12 rounded-xl bg-white/50 border border-slate-200 text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-pacific-500/20 focus:border-pacific-500"
                    disabled={isSubmitting}
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 p-1 text-slate-400 hover:text-slate-600"
                  >
                    {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                  </button>
                </div>
              </div>
            </div>

            {/* Security note */}
            <div className="mb-6 p-3 rounded-xl bg-pacific-50 border border-pacific-200">
              <div className="flex items-start gap-2">
                <Shield className="h-4 w-4 text-pacific-600 mt-0.5 flex-shrink-0" />
                <p className="text-xs text-pacific-700">
                  <strong>🔒 Conexión segura:</strong> Tus credenciales no se almacenan. Solo se usan para esta sincronización.
                </p>
              </div>
            </div>

            <div className="flex gap-3">
              <Button
                variant="outline"
                className="flex-1"
                onClick={() => setShowLoginModal(false)}
                disabled={isSubmitting}
              >
                Cancelar
              </Button>
              <Button
                variant="pacific"
                className="flex-1"
                onClick={handleSubmitLogin}
                disabled={isSubmitting || !rut || !password}
              >
                {isSubmitting ? (
                  <>
                    <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                    Conectando...
                  </>
                ) : (
                  'Conectar'
                )}
              </Button>
            </div>

            <p className="mt-4 text-xs text-center text-slate-500">
              Es la misma clave del SII, Registro Civil, Fonasa y otros servicios del Estado.
            </p>
          </div>
        </div>
      )}
    </RoleGuard>
  )
}
