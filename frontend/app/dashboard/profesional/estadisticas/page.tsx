'use client'

import { BarChart3, TrendingUp, Users, DollarSign, Clock, Star } from 'lucide-react'
import { RoleGuard, PageHeader, StatsCard } from '@/components/dashboard'

export default function EstadisticasPage() {
  return (
    <RoleGuard allowedRole="lawyer">
      <PageHeader
        title="Estadisticas"
        description="Metricas y rendimiento de tu perfil"
        icon={BarChart3}
      />

      {/* Overview Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatsCard
          title="Ingresos Totales"
          value="$0"
          description="Este mes"
          icon={DollarSign}
          variant="success"
        />
        <StatsCard
          title="Clientes Nuevos"
          value={0}
          description="Este mes"
          icon={Users}
          variant="pacific"
        />
        <StatsCard
          title="Tiempo Respuesta"
          value="--"
          description="Promedio"
          icon={Clock}
        />
        <StatsCard
          title="Valoracion"
          value="--/5"
          description="Promedio"
          icon={Star}
        />
      </div>

      {/* Charts Placeholder */}
      <div className="grid lg:grid-cols-2 gap-6 mb-8">
        <div className="glass-card rounded-2xl p-6">
          <h2 className="text-lg font-semibold text-slate-900 mb-4">
            Ingresos por Mes
          </h2>
          <div className="h-64 flex items-center justify-center bg-slate-50 rounded-xl">
            <div className="text-center">
              <BarChart3 className="h-12 w-12 text-slate-300 mx-auto mb-2" />
              <p className="text-sm text-slate-500">Grafico disponible proximamente</p>
            </div>
          </div>
        </div>

        <div className="glass-card rounded-2xl p-6">
          <h2 className="text-lg font-semibold text-slate-900 mb-4">
            Consultas por Especialidad
          </h2>
          <div className="h-64 flex items-center justify-center bg-slate-50 rounded-xl">
            <div className="text-center">
              <TrendingUp className="h-12 w-12 text-slate-300 mx-auto mb-2" />
              <p className="text-sm text-slate-500">Grafico disponible proximamente</p>
            </div>
          </div>
        </div>
      </div>

      {/* Performance Metrics */}
      <div className="glass-card rounded-2xl p-6">
        <h2 className="text-lg font-semibold text-slate-900 mb-4">
          Metricas de Rendimiento
        </h2>
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="p-4 rounded-xl bg-white/50">
            <p className="text-sm text-slate-500">Tasa de Aceptacion</p>
            <p className="text-2xl font-bold text-slate-900">--%</p>
            <p className="text-xs text-slate-400 mt-1">de solicitudes</p>
          </div>
          <div className="p-4 rounded-xl bg-white/50">
            <p className="text-sm text-slate-500">Casos Completados</p>
            <p className="text-2xl font-bold text-slate-900">0</p>
            <p className="text-xs text-slate-400 mt-1">este mes</p>
          </div>
          <div className="p-4 rounded-xl bg-white/50">
            <p className="text-sm text-slate-500">Clientes Recurrentes</p>
            <p className="text-2xl font-bold text-slate-900">0%</p>
            <p className="text-xs text-slate-400 mt-1">del total</p>
          </div>
          <div className="p-4 rounded-xl bg-white/50">
            <p className="text-sm text-slate-500">Resenas Positivas</p>
            <p className="text-2xl font-bold text-slate-900">0</p>
            <p className="text-xs text-slate-400 mt-1">de 0 totales</p>
          </div>
        </div>
      </div>
    </RoleGuard>
  )
}
