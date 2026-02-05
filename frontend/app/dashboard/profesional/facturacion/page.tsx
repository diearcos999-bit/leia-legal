'use client'

import { Receipt, Download, Filter, DollarSign, TrendingUp, CreditCard } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { RoleGuard, PageHeader, StatsCard, EmptyState } from '@/components/dashboard'

export default function FacturacionPage() {
  return (
    <RoleGuard allowedRole="lawyer">
      <PageHeader
        title="Facturacion"
        description="Ingresos, facturas y pagos"
        icon={Receipt}
        action={
          <div className="flex gap-2">
            <Button variant="outline" disabled>
              <Filter className="h-4 w-4 mr-2" />
              Filtrar
            </Button>
            <Button variant="outline" disabled>
              <Download className="h-4 w-4 mr-2" />
              Exportar
            </Button>
          </div>
        }
      />

      {/* Financial Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatsCard
          title="Ingresos del Mes"
          value="$0"
          description="CLP"
          icon={DollarSign}
          variant="success"
        />
        <StatsCard
          title="Pendiente de Cobro"
          value="$0"
          description="Por recibir"
          icon={CreditCard}
          variant="warning"
        />
        <StatsCard
          title="Total Historico"
          value="$0"
          description="CLP"
          icon={TrendingUp}
          variant="pacific"
        />
        <StatsCard
          title="Facturas Emitidas"
          value={0}
          description="Este mes"
          icon={Receipt}
        />
      </div>

      {/* Transactions Table Placeholder */}
      <div className="glass-card rounded-2xl p-6 mb-6">
        <h2 className="text-lg font-semibold text-slate-900 mb-4">
          Ultimas Transacciones
        </h2>

        <EmptyState
          icon={Receipt}
          title="Sin transacciones"
          description="Tus ingresos por consultas y servicios apareceran aqui cuando recibas pagos."
        />
      </div>

      {/* Payout Settings */}
      <div className="glass-card rounded-2xl p-6">
        <h2 className="text-lg font-semibold text-slate-900 mb-4">
          Configuracion de Pagos
        </h2>

        <div className="grid sm:grid-cols-2 gap-4">
          <div className="p-4 rounded-xl bg-white/50">
            <p className="text-sm text-slate-500 mb-1">Metodo de Pago</p>
            <p className="font-medium text-slate-900">No configurado</p>
          </div>
          <div className="p-4 rounded-xl bg-white/50">
            <p className="text-sm text-slate-500 mb-1">Frecuencia de Retiro</p>
            <p className="font-medium text-slate-900">No configurado</p>
          </div>
        </div>

        <p className="text-sm text-slate-500 mt-4">
          La configuracion de metodos de pago estara disponible proximamente.
        </p>
      </div>
    </RoleGuard>
  )
}
