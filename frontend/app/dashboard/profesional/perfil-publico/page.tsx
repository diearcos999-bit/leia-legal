'use client'

import { UserCircle, Mail, MapPin, Briefcase, Star, Eye } from 'lucide-react'
import { useAuth } from '@/lib/auth'
import { RoleGuard, PageHeader, StatsCard } from '@/components/dashboard'

export default function PerfilPublicoPage() {
  const { user } = useAuth()

  return (
    <RoleGuard allowedRole="lawyer">
      <PageHeader
        title="Mi Perfil Publico"
        description="Como te ven los clientes potenciales"
        icon={UserCircle}
      />

      {/* Profile Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatsCard
          title="Visitas al Perfil"
          value={0}
          description="Este mes"
          icon={Eye}
          variant="pacific"
        />
        <StatsCard
          title="Valoracion"
          value="--"
          description="Promedio"
          icon={Star}
        />
        <StatsCard
          title="Completado"
          value="20%"
          description="Del perfil"
          variant="warning"
        />
        <StatsCard
          title="Consultas"
          value={0}
          description="Recibidas"
        />
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Profile Preview */}
        <div className="lg:col-span-2">
          <div className="glass-card rounded-2xl p-6">
            <h2 className="text-lg font-semibold text-slate-900 mb-4">
              Vista Previa del Perfil
            </h2>

            <div className="flex items-start gap-4 mb-6">
              <div className="w-24 h-24 rounded-2xl bg-terracota-100 flex items-center justify-center flex-shrink-0">
                <UserCircle className="h-12 w-12 text-terracota-600" />
              </div>
              <div>
                <h3 className="text-xl font-semibold text-slate-900">
                  {user?.full_name || 'Nombre no configurado'}
                </h3>
                <p className="text-slate-500">Abogado/a</p>
                <div className="flex items-center gap-2 mt-2">
                  <MapPin className="h-4 w-4 text-slate-400" />
                  <span className="text-sm text-slate-500">Ubicacion no configurada</span>
                </div>
              </div>
            </div>

            <div className="space-y-4">
              <div>
                <h4 className="font-medium text-slate-900 mb-2">Sobre mi</h4>
                <p className="text-sm text-slate-500 italic">
                  Agrega una descripcion profesional para que los clientes te conozcan mejor.
                </p>
              </div>

              <div>
                <h4 className="font-medium text-slate-900 mb-2">Especialidades</h4>
                <p className="text-sm text-slate-500 italic">
                  No has agregado especialidades aun.
                </p>
              </div>

              <div>
                <h4 className="font-medium text-slate-900 mb-2">Experiencia</h4>
                <p className="text-sm text-slate-500 italic">
                  Agrega tu experiencia profesional.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Profile Completion */}
        <div>
          <div className="glass-card rounded-2xl p-6">
            <h2 className="text-lg font-semibold text-slate-900 mb-4">
              Completa tu Perfil
            </h2>

            <div className="space-y-3">
              {[
                { label: 'Foto de perfil', completed: false },
                { label: 'Descripcion profesional', completed: false },
                { label: 'Especialidades', completed: false },
                { label: 'Experiencia laboral', completed: false },
                { label: 'Tarifas', completed: false },
                { label: 'Horarios de atencion', completed: false },
                { label: 'Ubicacion/despacho', completed: false },
                { label: 'Certificaciones', completed: false },
              ].map((item) => (
                <div
                  key={item.label}
                  className="flex items-center gap-3 p-2 rounded-lg"
                >
                  <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center ${
                    item.completed
                      ? 'bg-green-500 border-green-500'
                      : 'border-slate-300'
                  }`}>
                    {item.completed && (
                      <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                    )}
                  </div>
                  <span className={`text-sm ${
                    item.completed ? 'text-slate-900' : 'text-slate-500'
                  }`}>
                    {item.label}
                  </span>
                </div>
              ))}
            </div>

            <p className="text-xs text-slate-500 mt-4">
              La edicion de perfil estara disponible proximamente.
            </p>
          </div>
        </div>
      </div>
    </RoleGuard>
  )
}
