'use client'

import { Bell } from 'lucide-react'
import { RoleGuard, PageHeader, EmptyState } from '@/components/dashboard'

export default function NotificacionesPage() {
  return (
    <RoleGuard allowedRole="user">
      <PageHeader
        title="Notificaciones"
        description="Alertas y avisos importantes"
        icon={Bell}
      />

      <EmptyState
        icon={Bell}
        title="Sin notificaciones"
        description="No tienes notificaciones nuevas. Te avisaremos cuando haya algo importante."
      />
    </RoleGuard>
  )
}
