'use client'

import Link from 'next/link'
import { Scale, Plus } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { RoleGuard, PageHeader, EmptyState } from '@/components/dashboard'

export default function ConsultasAbogadosPage() {
  return (
    <RoleGuard allowedRole="user">
      <PageHeader
        title="Consultas a Abogados"
        description="Consultas con profesionales verificados"
        icon={Scale}
        action={
          <Button variant="pacific" asChild>
            <Link href="/abogados">
              <Plus className="h-4 w-4 mr-2" />
              Buscar Abogado
            </Link>
          </Button>
        }
      />

      <EmptyState
        icon={Scale}
        title="Sin consultas a abogados"
        description="Aun no has realizado consultas con abogados. Encuentra un profesional para tu caso."
        action={{
          label: 'Explorar Abogados',
          href: '/abogados'
        }}
      />
    </RoleGuard>
  )
}
