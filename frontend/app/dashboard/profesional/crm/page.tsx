'use client'

import { Users, Plus, Search } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { RoleGuard, PageHeader, EmptyState } from '@/components/dashboard'

export default function CRMPage() {
  return (
    <RoleGuard allowedRole="lawyer">
      <PageHeader
        title="CRM Clientes"
        description="Gestiona tu cartera de clientes"
        icon={Users}
        action={
          <Button variant="pacific" disabled>
            <Plus className="h-4 w-4 mr-2" />
            Agregar Cliente
          </Button>
        }
      />

      {/* Search Bar */}
      <div className="glass-card rounded-2xl p-4 mb-6">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-slate-400" />
          <input
            type="text"
            placeholder="Buscar cliente por nombre o email..."
            className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-white/50 border border-white/40 text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-pacific-500/20 focus:border-pacific-500"
            disabled
          />
        </div>
      </div>

      <EmptyState
        icon={Users}
        title="Sin clientes registrados"
        description="Tu cartera de clientes aparecera aqui. Cuando recibas consultas y las aceptes, podras gestionar tus clientes desde este panel."
      />
    </RoleGuard>
  )
}
