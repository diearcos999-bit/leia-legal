'use client'

import Link from 'next/link'
import { Inbox, Users, Briefcase, Calendar, Receipt, ArrowRight, TrendingUp, ClipboardList, Building2, Scale, Gavel } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { useAuth } from '@/lib/auth'
import { useRole } from '@/lib/hooks/useRole'
import { RoleGuard, PageHeader, StatsCard, EmptyState } from '@/components/dashboard'

export default function ProfesionalHomePage() {
  const { user } = useAuth()
  const { professionalType, roleDescription } = useRole()
  const firstName = user?.full_name?.split(' ')[0] || 'Profesional'

  // Get dashboard subtitle based on professional type
  const getSubtitle = () => {
    switch (professionalType) {
      case 'procurador':
        return 'Panel de gestion de tramites judiciales'
      case 'estudio':
        return 'Panel de administracion del estudio'
      default:
        return 'Bienvenido a tu panel profesional'
    }
  }

  return (
    <RoleGuard allowedRole="lawyer">
      <PageHeader
        title={`Hola, ${firstName}`}
        description={getSubtitle()}
      />

      {/* Stats Grid - varies by professional type */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatsCard
          title="Solicitudes Nuevas"
          value={0}
          description="Pendientes de respuesta"
          icon={Inbox}
          variant="terracota"
        />
        {professionalType === 'procurador' ? (
          <StatsCard
            title="Tramites Activos"
            value={0}
            description="En proceso"
            icon={ClipboardList}
            variant="pacific"
          />
        ) : professionalType === 'estudio' ? (
          <StatsCard
            title="Miembros del Equipo"
            value={0}
            description="Abogados y procuradores"
            icon={Users}
            variant="pacific"
          />
        ) : (
          <StatsCard
            title="Clientes Activos"
            value={0}
            description="En tu cartera"
            icon={Users}
            variant="pacific"
          />
        )}
        <StatsCard
          title={professionalType === 'procurador' ? 'Diligencias' : 'Casos Abiertos'}
          value={0}
          description="En progreso"
          icon={Briefcase}
        />
        <StatsCard
          title="Ingresos del Mes"
          value="$0"
          description="CLP"
          icon={Receipt}
          variant="success"
        />
      </div>

      {/* Main Content Grid */}
      <div className="grid lg:grid-cols-2 gap-6 mb-8">
        {/* Recent Requests / Tramites */}
        <div className="glass-card rounded-2xl p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-slate-900">
              {professionalType === 'procurador' ? 'Tramites Pendientes' : 'Solicitudes Recientes'}
            </h2>
            <Button variant="ghost" size="sm" asChild>
              <Link href={professionalType === 'procurador' ? '/dashboard/profesional/tramites' : '/dashboard/profesional/solicitudes'}>
                Ver {professionalType === 'procurador' ? 'tramites' : 'todas'}
                <ArrowRight className="h-4 w-4 ml-1" />
              </Link>
            </Button>
          </div>
          <EmptyState
            icon={professionalType === 'procurador' ? ClipboardList : Inbox}
            title={professionalType === 'procurador' ? 'Sin tramites pendientes' : 'Sin solicitudes nuevas'}
            description={professionalType === 'procurador' ? 'Los tramites asignados apareceran aqui' : 'Las solicitudes de clientes apareceran aqui'}
          />
        </div>

        {/* Today's Schedule / Team (for estudio) */}
        <div className="glass-card rounded-2xl p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-slate-900">
              {professionalType === 'estudio' ? 'Equipo del Estudio' : 'Agenda de Hoy'}
            </h2>
            <Button variant="ghost" size="sm" asChild>
              <Link href={professionalType === 'estudio' ? '/dashboard/profesional/equipo' : '/dashboard/profesional/calendario'}>
                Ver {professionalType === 'estudio' ? 'equipo' : 'calendario'}
                <ArrowRight className="h-4 w-4 ml-1" />
              </Link>
            </Button>
          </div>
          <EmptyState
            icon={professionalType === 'estudio' ? Users : Calendar}
            title={professionalType === 'estudio' ? 'Sin miembros registrados' : 'Sin citas para hoy'}
            description={professionalType === 'estudio' ? 'Invita abogados y procuradores a tu estudio' : 'Tus proximas citas apareceran aqui'}
          />
        </div>
      </div>

      {/* Performance Overview */}
      <div className="glass-card rounded-2xl p-6 mb-8">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-slate-900">
            Resumen de Rendimiento
          </h2>
          <Button variant="ghost" size="sm" asChild>
            <Link href="/dashboard/profesional/estadisticas">
              Ver estadisticas
              <ArrowRight className="h-4 w-4 ml-1" />
            </Link>
          </Button>
        </div>
        <div className="grid sm:grid-cols-3 gap-4">
          <div className="p-4 rounded-xl bg-white/50">
            <p className="text-sm text-slate-500">Tasa de Respuesta</p>
            <p className="text-2xl font-bold text-slate-900">--%</p>
          </div>
          <div className="p-4 rounded-xl bg-white/50">
            <p className="text-sm text-slate-500">Valoracion Promedio</p>
            <p className="text-2xl font-bold text-slate-900">-- / 5</p>
          </div>
          <div className="p-4 rounded-xl bg-white/50">
            <p className="text-sm text-slate-500">Casos Completados</p>
            <p className="text-2xl font-bold text-slate-900">0</p>
          </div>
        </div>
      </div>

      {/* CTA Banner */}
      <div className="glass-card rounded-2xl p-6 bg-gradient-to-br from-terracota-50 to-white border-terracota-100">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-terracota-100">
              <TrendingUp className="h-6 w-6 text-terracota-600" />
            </div>
            <div>
              <h3 className="font-semibold text-slate-900">
                Completa tu perfil publico
              </h3>
              <p className="text-sm text-slate-600">
                Un perfil completo aumenta tus consultas en un 80%
              </p>
            </div>
          </div>
          <Button variant="pacific" asChild>
            <Link href="/dashboard/profesional/perfil-publico">
              Completar Perfil
              <ArrowRight className="h-4 w-4 ml-2" />
            </Link>
          </Button>
        </div>
      </div>
    </RoleGuard>
  )
}
