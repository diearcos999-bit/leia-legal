'use client'

import { Search } from 'lucide-react'
import { RoleGuard, PageHeader, EmptyState } from '@/components/dashboard'

export default function SeguimientoCasosPage() {
  return (
    <RoleGuard allowedRole="user">
      <PageHeader
        title="Seguimiento de Casos"
        description="Estado de tus casos legales"
        icon={Search}
      />

      <EmptyState
        icon={Search}
        title="Sin casos activos"
        description="No tienes casos en seguimiento. Cuando contrates un abogado, podras ver el estado de tu caso aqui."
      />
    </RoleGuard>
  )
}
