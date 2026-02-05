'use client'

import { Bookmark } from 'lucide-react'
import { RoleGuard, PageHeader, EmptyState } from '@/components/dashboard'

export default function ConsultasGuardadasPage() {
  return (
    <RoleGuard allowedRole="user">
      <PageHeader
        title="Consultas Guardadas"
        description="Respuestas y consultas que has guardado"
        icon={Bookmark}
      />

      <EmptyState
        icon={Bookmark}
        title="Sin consultas guardadas"
        description="Guarda respuestas importantes de LEIA para acceder a ellas facilmente mas tarde."
        action={{
          label: 'Ir a Conversaciones',
          href: '/dashboard/usuario/conversaciones'
        }}
      />
    </RoleGuard>
  )
}
