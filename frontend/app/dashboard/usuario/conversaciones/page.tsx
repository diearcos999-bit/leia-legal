'use client'

import Link from 'next/link'
import { MessageSquare, Plus } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { RoleGuard, PageHeader, EmptyState } from '@/components/dashboard'

export default function ConversacionesPage() {
  return (
    <RoleGuard allowedRole="user">
      <PageHeader
        title="Mis Conversaciones"
        description="Historial de chats con LEIA"
        icon={MessageSquare}
        action={
          <Button variant="pacific" asChild>
            <Link href="/chat">
              <Plus className="h-4 w-4 mr-2" />
              Nueva Consulta
            </Link>
          </Button>
        }
      />

      <EmptyState
        icon={MessageSquare}
        title="Sin conversaciones"
        description="Aun no has iniciado ninguna conversacion con LEIA. Comienza ahora y obtén orientación legal inmediata."
        action={{
          label: 'Iniciar Consulta',
          href: '/chat'
        }}
      />
    </RoleGuard>
  )
}
