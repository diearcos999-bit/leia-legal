'use client'

import { useState, useEffect } from 'react'
import { useAuth } from '@/lib/auth'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { RoleGuard, PageHeader } from '@/components/dashboard'
import {
  Settings,
  MessageSquare,
  Phone,
  Video,
  Clock,
  Save,
  Loader2,
  CheckCircle,
  AlertTriangle
} from 'lucide-react'
import { cn } from '@/lib/utils'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface CommunicationSettings {
  chat_enabled: boolean
  voice_enabled: boolean
  video_enabled: boolean
  available_hours?: Record<string, { start: string; end: string }>
  response_time_target: number
  is_available: boolean
  unavailable_until?: string
  unavailable_message?: string
}

const defaultAvailableHours = {
  monday: { start: '09:00', end: '18:00' },
  tuesday: { start: '09:00', end: '18:00' },
  wednesday: { start: '09:00', end: '18:00' },
  thursday: { start: '09:00', end: '18:00' },
  friday: { start: '09:00', end: '18:00' },
  saturday: { start: '', end: '' },
  sunday: { start: '', end: '' }
}

const dayNames: Record<string, string> = {
  monday: 'Lunes',
  tuesday: 'Martes',
  wednesday: 'Miércoles',
  thursday: 'Jueves',
  friday: 'Viernes',
  saturday: 'Sábado',
  sunday: 'Domingo'
}

export default function ConfiguracionPage() {
  const { token } = useAuth()
  const [settings, setSettings] = useState<CommunicationSettings>({
    chat_enabled: true,
    voice_enabled: false,
    video_enabled: false,
    available_hours: defaultAvailableHours,
    response_time_target: 24,
    is_available: true
  })
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)

  useEffect(() => {
    const fetchSettings = async () => {
      if (!token) return

      try {
        const response = await fetch(`${API_URL}/api/calls/settings`, {
          headers: { 'Authorization': `Bearer ${token}` }
        })

        if (response.ok) {
          const data = await response.json()
          setSettings({
            ...data,
            available_hours: data.available_hours || defaultAvailableHours
          })
          setError(null)
        } else if (response.status === 403) {
          setError('Solo los abogados pueden acceder a esta configuración')
        }
      } catch (err) {
        setError('Error de conexión')
      } finally {
        setIsLoading(false)
      }
    }

    fetchSettings()
  }, [token])

  const saveSettings = async () => {
    if (!token) return

    setIsSaving(true)
    setError(null)
    setSuccess(false)

    try {
      const response = await fetch(`${API_URL}/api/calls/settings`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(settings)
      })

      if (response.ok) {
        setSuccess(true)
        setTimeout(() => setSuccess(false), 3000)
      } else {
        const data = await response.json()
        setError(data.detail || 'Error al guardar configuración')
      }
    } catch (err) {
      setError('Error de conexión')
    } finally {
      setIsSaving(false)
    }
  }

  const updateHours = (day: string, field: 'start' | 'end', value: string) => {
    setSettings(prev => ({
      ...prev,
      available_hours: {
        ...prev.available_hours,
        [day]: {
          ...(prev.available_hours?.[day] || { start: '', end: '' }),
          [field]: value
        }
      }
    }))
  }

  const ToggleSwitch = ({
    enabled,
    onChange,
    label,
    description,
    icon: Icon
  }: {
    enabled: boolean
    onChange: (enabled: boolean) => void
    label: string
    description: string
    icon: React.ElementType
  }) => (
    <div className="flex items-center justify-between p-4 bg-slate-50 rounded-lg">
      <div className="flex items-center gap-3">
        <div className={cn(
          'w-10 h-10 rounded-lg flex items-center justify-center',
          enabled ? 'bg-pacific-100 text-pacific-600' : 'bg-slate-200 text-slate-500'
        )}>
          <Icon className="h-5 w-5" />
        </div>
        <div>
          <p className="font-medium text-slate-900">{label}</p>
          <p className="text-sm text-slate-500">{description}</p>
        </div>
      </div>
      <button
        onClick={() => onChange(!enabled)}
        className={cn(
          'relative w-12 h-6 rounded-full transition-colors',
          enabled ? 'bg-pacific-500' : 'bg-slate-300'
        )}
      >
        <span
          className={cn(
            'absolute top-1 w-4 h-4 rounded-full bg-white transition-transform',
            enabled ? 'translate-x-7' : 'translate-x-1'
          )}
        />
      </button>
    </div>
  )

  if (isLoading) {
    return (
      <RoleGuard allowedRole="lawyer">
        <div className="flex items-center justify-center py-12">
          <Loader2 className="h-8 w-8 animate-spin text-pacific-500" />
        </div>
      </RoleGuard>
    )
  }

  return (
    <RoleGuard allowedRole="lawyer">
      <PageHeader
        title="Configuración"
        description="Gestiona tus preferencias de comunicación con clientes"
        icon={Settings}
      />

      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center gap-3 text-red-700">
          <AlertTriangle className="h-5 w-5" />
          {error}
        </div>
      )}

      {success && (
        <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg flex items-center gap-3 text-green-700">
          <CheckCircle className="h-5 w-5" />
          Configuración guardada correctamente
        </div>
      )}

      <div className="space-y-6">
        {/* Communication methods */}
        <div className="glass-card rounded-xl p-6">
          <h2 className="font-semibold text-slate-900 mb-4">Métodos de Comunicación</h2>
          <p className="text-sm text-slate-600 mb-4">
            Habilita los métodos de comunicación que deseas ofrecer a tus clientes
          </p>

          <div className="space-y-3">
            <ToggleSwitch
              enabled={settings.chat_enabled}
              onChange={(enabled) => setSettings(prev => ({ ...prev, chat_enabled: enabled }))}
              label="Chat de texto"
              description="Permite que los clientes te envíen mensajes de texto"
              icon={MessageSquare}
            />

            <ToggleSwitch
              enabled={settings.voice_enabled}
              onChange={(enabled) => setSettings(prev => ({ ...prev, voice_enabled: enabled }))}
              label="Llamadas de voz"
              description="Permite que los clientes te llamen por voz"
              icon={Phone}
            />

            <ToggleSwitch
              enabled={settings.video_enabled}
              onChange={(enabled) => setSettings(prev => ({ ...prev, video_enabled: enabled }))}
              label="Videollamadas"
              description="Permite videollamadas con clientes"
              icon={Video}
            />
          </div>

          {(settings.voice_enabled || settings.video_enabled) && (
            <div className="mt-4 p-4 bg-pacific-50 rounded-lg">
              <p className="text-sm text-pacific-700">
                <strong>Nota:</strong> Las llamadas se realizan a través de nuestra plataforma,
                sin compartir tu número de teléfono personal.
              </p>
            </div>
          )}
        </div>

        {/* Availability */}
        <div className="glass-card rounded-xl p-6">
          <h2 className="font-semibold text-slate-900 mb-4">Disponibilidad</h2>

          <div className="mb-6">
            <ToggleSwitch
              enabled={settings.is_available}
              onChange={(enabled) => setSettings(prev => ({ ...prev, is_available: enabled }))}
              label="Disponible para nuevos casos"
              description={settings.is_available
                ? "Los clientes pueden enviarte solicitudes"
                : "No recibirás nuevas solicitudes"
              }
              icon={Clock}
            />
          </div>

          {!settings.is_available && (
            <div className="mb-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Fecha de regreso (opcional)
                </label>
                <Input
                  type="date"
                  value={settings.unavailable_until?.split('T')[0] || ''}
                  onChange={(e) => setSettings(prev => ({
                    ...prev,
                    unavailable_until: e.target.value ? new Date(e.target.value).toISOString() : undefined
                  }))}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Mensaje para clientes (opcional)
                </label>
                <textarea
                  value={settings.unavailable_message || ''}
                  onChange={(e) => setSettings(prev => ({
                    ...prev,
                    unavailable_message: e.target.value
                  }))}
                  className="w-full p-3 border border-slate-200 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-pacific-500"
                  rows={2}
                  placeholder="Ej: Estaré de vacaciones hasta el 15 de enero..."
                />
              </div>
            </div>
          )}

          {/* Response time target */}
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              Objetivo de tiempo de respuesta
            </label>
            <div className="flex items-center gap-3">
              <select
                value={settings.response_time_target}
                onChange={(e) => setSettings(prev => ({
                  ...prev,
                  response_time_target: parseInt(e.target.value)
                }))}
                className="p-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-pacific-500"
              >
                <option value={2}>2 horas</option>
                <option value={4}>4 horas</option>
                <option value={8}>8 horas</option>
                <option value={24}>24 horas</option>
                <option value={48}>48 horas</option>
              </select>
              <p className="text-sm text-slate-500">
                Los clientes verán este tiempo estimado de respuesta
              </p>
            </div>
          </div>
        </div>

        {/* Available hours */}
        <div className="glass-card rounded-xl p-6">
          <h2 className="font-semibold text-slate-900 mb-4">Horarios de Atención</h2>
          <p className="text-sm text-slate-600 mb-4">
            Define tus horarios de disponibilidad para llamadas
          </p>

          <div className="space-y-3">
            {Object.entries(dayNames).map(([day, dayName]) => (
              <div key={day} className="flex items-center gap-4">
                <span className="w-24 text-sm font-medium text-slate-700">
                  {dayName}
                </span>
                <Input
                  type="time"
                  value={settings.available_hours?.[day]?.start || ''}
                  onChange={(e) => updateHours(day, 'start', e.target.value)}
                  className="w-32"
                  placeholder="Inicio"
                />
                <span className="text-slate-400">a</span>
                <Input
                  type="time"
                  value={settings.available_hours?.[day]?.end || ''}
                  onChange={(e) => updateHours(day, 'end', e.target.value)}
                  className="w-32"
                  placeholder="Fin"
                />
                {!settings.available_hours?.[day]?.start && (
                  <span className="text-xs text-slate-400">No disponible</span>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Save button */}
        <div className="flex justify-end">
          <Button
            variant="pacific"
            onClick={saveSettings}
            disabled={isSaving}
            className="min-w-[150px]"
          >
            {isSaving ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <>
                <Save className="h-4 w-4 mr-2" />
                Guardar cambios
              </>
            )}
          </Button>
        </div>
      </div>
    </RoleGuard>
  )
}
