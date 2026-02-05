'use client'

import Link from 'next/link'
import { MessageSquare, Scale, FileText, Bell, Calendar, ArrowRight } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { useAuth } from '@/lib/auth'
import { RoleGuard, PageHeader, StatsCard, EmptyState } from '@/components/dashboard'

export default function UsuarioHomePage() {
  const { user } = useAuth()
  const firstName = user?.full_name?.split(' ')[0] || 'Usuario'

  return (
    <RoleGuard allowedRole="user">
      <PageHeader
        title={`Hola, ${firstName}`}
        description="Bienvenido a tu panel de control"
      />

      {/* Stats Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatsCard
          title="Consultas IA"
          value={0}
          description="Chats con LEIA"
          icon={MessageSquare}
          variant="pacific"
        />
        <StatsCard
          title="Consultas Abogados"
          value={0}
          description="Con profesionales"
          icon={Scale}
        />
        <StatsCard
          title="Documentos"
          value={0}
          description="Generados"
          icon={FileText}
        />
        <StatsCard
          title="Notificaciones"
          value={0}
          description="Sin leer"
          icon={Bell}
        />
      </div>

      {/* Quick Actions */}
      <div className="grid lg:grid-cols-2 gap-6 mb-8">
        {/* Recent Conversations */}
        <div className="glass-card rounded-2xl p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-slate-900">
              Conversaciones Recientes
            </h2>
            <Button variant="ghost" size="sm" asChild>
              <Link href="/dashboard/usuario/conversaciones">
                Ver todas
                <ArrowRight className="h-4 w-4 ml-1" />
              </Link>
            </Button>
          </div>
          <EmptyState
            icon={MessageSquare}
            title="Sin conversaciones"
            description="Inicia tu primera consulta con LEIA, nuestra asistente de IA legal"
            action={{
              label: 'Nueva Consulta',
              href: '/chat'
            }}
          />
        </div>

        {/* Upcoming Appointments */}
        <div className="glass-card rounded-2xl p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-slate-900">
              Proximas Citas
            </h2>
            <Button variant="ghost" size="sm" asChild>
              <Link href="/dashboard/usuario/citas">
                Ver todas
                <ArrowRight className="h-4 w-4 ml-1" />
              </Link>
            </Button>
          </div>
          <EmptyState
            icon={Calendar}
            title="Sin citas programadas"
            description="Agenda una consulta con un abogado verificado"
            action={{
              label: 'Buscar Abogado',
              href: '/abogados'
            }}
          />
        </div>
      </div>

      {/* CTA Banner */}
      <div className="glass-card rounded-2xl p-6 bg-gradient-to-br from-pacific-50 to-white border-pacific-100">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
          <div>
            <h3 className="font-semibold text-slate-900">
              Comienza a usar LEIA
            </h3>
            <p className="text-sm text-slate-600">
              Haz tu primera consulta legal con nuestro asistente de IA
            </p>
          </div>
          <Button variant="pacific" asChild>
            <Link href="/chat">
              Iniciar Consulta
              <ArrowRight className="h-4 w-4 ml-2" />
            </Link>
          </Button>
        </div>
      </div>
    </RoleGuard>
  )
}
