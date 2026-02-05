'use client'

import { useState, useEffect } from 'react'
import { useAuth } from '@/lib/auth'
import { Button } from '@/components/ui/button'
import { RoleGuard, PageHeader, EmptyState, StatsCard } from '@/components/dashboard'
import {
  Users,
  Scale,
  Gavel,
  UserPlus,
  Mail,
  Phone,
  Briefcase,
  Star,
  Loader2,
  MoreVertical
} from 'lucide-react'
import { cn } from '@/lib/utils'

interface TeamMember {
  id: number
  name: string
  email: string
  phone?: string
  professional_type: 'abogado' | 'procurador'
  specialty: string
  cases_active: number
  rating: number
  status: 'active' | 'inactive' | 'vacation'
  joined_at: string
}

const statusConfig: Record<string, { label: string; color: string }> = {
  active: { label: 'Activo', color: 'bg-green-100 text-green-700' },
  inactive: { label: 'Inactivo', color: 'bg-slate-100 text-slate-700' },
  vacation: { label: 'Vacaciones', color: 'bg-yellow-100 text-yellow-700' }
}

export default function EquipoPage() {
  const { token } = useAuth()
  const [members, setMembers] = useState<TeamMember[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [showInviteModal, setShowInviteModal] = useState(false)

  useEffect(() => {
    // Mock data - replace with API call when endpoint is ready
    const mockMembers: TeamMember[] = [
      {
        id: 1,
        name: 'Carlos Fernandez',
        email: 'carlos@estudio.cl',
        phone: '+56 9 1234 5678',
        professional_type: 'abogado',
        specialty: 'Derecho Laboral',
        cases_active: 12,
        rating: 4.8,
        status: 'active',
        joined_at: '2023-06-15'
      },
      {
        id: 2,
        name: 'Maria Torres',
        email: 'maria@estudio.cl',
        phone: '+56 9 8765 4321',
        professional_type: 'abogado',
        specialty: 'Derecho de Familia',
        cases_active: 8,
        rating: 4.9,
        status: 'active',
        joined_at: '2023-08-20'
      },
      {
        id: 3,
        name: 'Pedro Sanchez',
        email: 'pedro@estudio.cl',
        professional_type: 'procurador',
        specialty: 'Tramites Civiles',
        cases_active: 15,
        rating: 4.7,
        status: 'active',
        joined_at: '2024-01-10'
      },
      {
        id: 4,
        name: 'Ana Lopez',
        email: 'ana@estudio.cl',
        professional_type: 'abogado',
        specialty: 'Derecho Penal',
        cases_active: 0,
        rating: 4.5,
        status: 'vacation',
        joined_at: '2023-03-01'
      }
    ]

    setTimeout(() => {
      setMembers(mockMembers)
      setIsLoading(false)
    }, 500)
  }, [token])

  const totalAbogados = members.filter(m => m.professional_type === 'abogado').length
  const totalProcuradores = members.filter(m => m.professional_type === 'procurador').length
  const activeMembers = members.filter(m => m.status === 'active').length
  const totalCases = members.reduce((acc, m) => acc + m.cases_active, 0)

  return (
    <RoleGuard allowedRole="lawyer">
      <PageHeader
        title="Equipo del Estudio"
        description="Gestiona los abogados y procuradores de tu estudio juridico"
        icon={Users}
        action={
          <Button variant="pacific" onClick={() => setShowInviteModal(true)}>
            <UserPlus className="h-4 w-4 mr-2" />
            Invitar miembro
          </Button>
        }
      />

      {/* Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatsCard
          title="Abogados"
          value={totalAbogados}
          variant="pacific"
          icon={Scale}
        />
        <StatsCard
          title="Procuradores"
          value={totalProcuradores}
          icon={Gavel}
        />
        <StatsCard
          title="Activos"
          value={activeMembers}
          variant="success"
          icon={Users}
        />
        <StatsCard
          title="Casos totales"
          value={totalCases}
          variant="warning"
          icon={Briefcase}
        />
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="h-8 w-8 animate-spin text-pacific-500" />
        </div>
      ) : members.length === 0 ? (
        <EmptyState
          icon={Users}
          title="Sin miembros en el equipo"
          description="Invita abogados y procuradores para que se unan a tu estudio."
          action={{
            label: 'Invitar miembro',
            onClick: () => setShowInviteModal(true)
          }}
        />
      ) : (
        <div className="grid gap-4 md:grid-cols-2">
          {members.map((member) => {
            const status = statusConfig[member.status]
            const Icon = member.professional_type === 'abogado' ? Scale : Gavel

            return (
              <div
                key={member.id}
                className="glass-card rounded-xl p-4 hover:shadow-md transition-shadow"
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <div className={cn(
                      'w-12 h-12 rounded-full flex items-center justify-center',
                      member.professional_type === 'abogado'
                        ? 'bg-pacific-100'
                        : 'bg-terracota-100'
                    )}>
                      <Icon className={cn(
                        'h-6 w-6',
                        member.professional_type === 'abogado'
                          ? 'text-pacific-600'
                          : 'text-terracota-600'
                      )} />
                    </div>
                    <div>
                      <h3 className="font-medium text-slate-900">{member.name}</h3>
                      <p className="text-sm text-slate-500">
                        {member.professional_type === 'abogado' ? 'Abogado/a' : 'Procurador/a'}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className={cn(
                      'px-2 py-0.5 rounded-full text-xs font-medium',
                      status.color
                    )}>
                      {status.label}
                    </span>
                    <button className="p-1 hover:bg-slate-100 rounded">
                      <MoreVertical className="h-4 w-4 text-slate-400" />
                    </button>
                  </div>
                </div>

                {/* Specialty */}
                <div className="mb-3">
                  <span className="inline-block px-2 py-1 bg-slate-100 rounded text-xs text-slate-600">
                    {member.specialty}
                  </span>
                </div>

                {/* Contact */}
                <div className="flex flex-wrap gap-3 text-xs text-slate-500 mb-3">
                  <span className="flex items-center gap-1">
                    <Mail className="h-3 w-3" />
                    {member.email}
                  </span>
                  {member.phone && (
                    <span className="flex items-center gap-1">
                      <Phone className="h-3 w-3" />
                      {member.phone}
                    </span>
                  )}
                </div>

                {/* Stats */}
                <div className="flex items-center justify-between pt-3 border-t border-slate-100">
                  <div className="flex items-center gap-1 text-sm">
                    <Briefcase className="h-4 w-4 text-slate-400" />
                    <span className="font-medium text-slate-700">{member.cases_active}</span>
                    <span className="text-slate-500">casos activos</span>
                  </div>
                  <div className="flex items-center gap-1 text-sm">
                    <Star className="h-4 w-4 text-yellow-500 fill-yellow-500" />
                    <span className="font-medium text-slate-700">{member.rating}</span>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      )}

      {/* TODO: Add invite modal */}
    </RoleGuard>
  )
}
