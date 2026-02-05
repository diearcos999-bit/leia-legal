'use client'

import { FileText } from 'lucide-react'
import { RoleGuard, PageHeader, EmptyState } from '@/components/dashboard'

export default function DocumentosPage() {
  return (
    <RoleGuard allowedRole="user">
      <PageHeader
        title="Documentos"
        description="Documentos legales generados"
        icon={FileText}
      />

      <EmptyState
        icon={FileText}
        title="Sin documentos"
        description="Los documentos generados con LEIA apareceran aqui. Esta funcion estara disponible proximamente."
      />
    </RoleGuard>
  )
}
