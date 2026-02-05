'use client'

import Link from 'next/link'
import { Calendar, Plus } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { RoleGuard, PageHeader, EmptyState } from '@/components/dashboard'

export default function CitasPage() {
  return (
    <RoleGuard allowedRole="user">
      <PageHeader
        title="Citas"
        description="Citas programadas con abogados"
        icon={Calendar}
        action={
          <Button variant="pacific" asChild>
            <Link href="/abogados">
              <Plus className="h-4 w-4 mr-2" />
              Agendar Cita
            </Link>
          </Button>
        }
      />

      <EmptyState
        icon={Calendar}
        title="Sin citas programadas"
        description="No tienes citas agendadas. Busca un abogado y agenda una consulta."
        action={{
          label: 'Buscar Abogado',
          href: '/abogados'
        }}
      />
    </RoleGuard>
  )
}
