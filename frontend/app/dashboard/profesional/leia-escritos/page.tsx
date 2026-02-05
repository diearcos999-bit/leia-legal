'use client'

import { Sparkles, FileText, Plus, Wand2 } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { RoleGuard, PageHeader, EmptyState } from '@/components/dashboard'

export default function LeiaEscritosPage() {
  return (
    <RoleGuard allowedRole="lawyer">
      <PageHeader
        title="LEIA Escritos"
        description="Genera documentos legales con IA"
        icon={Sparkles}
        action={
          <Button variant="pacific" disabled>
            <Plus className="h-4 w-4 mr-2" />
            Nuevo Documento
          </Button>
        }
      />

      {/* Feature Cards */}
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
        <div className="glass-card rounded-2xl p-5">
          <div className="p-2.5 rounded-xl bg-pacific-100 w-fit mb-3">
            <FileText className="h-5 w-5 text-pacific-600" />
          </div>
          <h3 className="font-semibold text-slate-900 mb-1">Contratos</h3>
          <p className="text-sm text-slate-500">
            Genera contratos personalizados con clausulas optimizadas
          </p>
        </div>

        <div className="glass-card rounded-2xl p-5">
          <div className="p-2.5 rounded-xl bg-terracota-100 w-fit mb-3">
            <FileText className="h-5 w-5 text-terracota-600" />
          </div>
          <h3 className="font-semibold text-slate-900 mb-1">Demandas</h3>
          <p className="text-sm text-slate-500">
            Redacta demandas con estructura y formato correcto
          </p>
        </div>

        <div className="glass-card rounded-2xl p-5">
          <div className="p-2.5 rounded-xl bg-amber-100 w-fit mb-3">
            <FileText className="h-5 w-5 text-amber-600" />
          </div>
          <h3 className="font-semibold text-slate-900 mb-1">Recursos</h3>
          <p className="text-sm text-slate-500">
            Crea recursos de apelacion y otros escritos judiciales
          </p>
        </div>
      </div>

      <EmptyState
        icon={Wand2}
        title="Proximamente"
        description="LEIA Escritos te permitira generar documentos legales profesionales con inteligencia artificial. Esta funcion estara disponible pronto."
      />
    </RoleGuard>
  )
}
