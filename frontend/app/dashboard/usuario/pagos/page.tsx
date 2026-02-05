'use client'

import { CreditCard } from 'lucide-react'
import { RoleGuard, PageHeader, EmptyState } from '@/components/dashboard'

export default function PagosPage() {
  return (
    <RoleGuard allowedRole="user">
      <PageHeader
        title="Pagos y Facturas"
        description="Historial de pagos y facturas"
        icon={CreditCard}
      />

      <EmptyState
        icon={CreditCard}
        title="Sin transacciones"
        description="No tienes pagos registrados. Tus transacciones apareceran aqui cuando realices una contratacion."
      />
    </RoleGuard>
  )
}
