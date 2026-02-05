'use client'

import { User, Building2, Scale, Gavel } from 'lucide-react'
import { useAuth } from '@/lib/auth'
import { useRole } from '@/lib/hooks/useRole'

export function SidebarUserInfo() {
  const { user } = useAuth()
  const { roleDescription, isLawyer, professionalType } = useRole()

  if (!user) return null

  // Get icon based on professional type
  const getIcon = () => {
    if (!isLawyer) return User
    switch (professionalType) {
      case 'procurador':
        return Gavel
      case 'estudio':
        return Building2
      case 'abogado':
      default:
        return Scale
    }
  }

  const Icon = getIcon()

  return (
    <div className="p-4 border-b border-white/10">
      <div className="flex items-center gap-3 p-3 rounded-xl bg-white/40">
        <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
          isLawyer ? 'bg-terracota-100' : 'bg-pacific-100'
        }`}>
          <Icon className={`h-5 w-5 ${
            isLawyer ? 'text-terracota-600' : 'text-pacific-600'
          }`} />
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-sm font-medium text-slate-900 truncate">
            {user.full_name || 'Usuario'}
          </p>
          <p className={`text-xs ${
            isLawyer ? 'text-terracota-600' : 'text-pacific-600'
          }`}>
            {roleDescription}
          </p>
        </div>
      </div>
    </div>
  )
}
