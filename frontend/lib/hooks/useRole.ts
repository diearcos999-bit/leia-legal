'use client'

import { useAuth, ProfessionalType } from '@/lib/auth'
import {
  userNavigation,
  getNavigationByProfessionalType,
  getProfessionalTypeLabel,
  type NavItem
} from '@/lib/config/navigation'

export type UserRole = 'user' | 'lawyer'

export interface RoleInfo {
  role: UserRole
  isUser: boolean
  isLawyer: boolean
  professionalType: ProfessionalType
  navigation: NavItem[]
  dashboardHome: string
  roleLabel: string
  roleDescription: string
  isLoading: boolean
}

export function useRole(): RoleInfo {
  const { user, professionalType, isLoading } = useAuth()

  const role = (user?.role as UserRole) || 'user'
  const isLawyer = role === 'lawyer'

  // Get navigation based on role and professional type
  const navigation = isLawyer
    ? getNavigationByProfessionalType(professionalType)
    : userNavigation

  // Get role description based on professional type
  const roleDescription = isLawyer
    ? getProfessionalTypeLabel(professionalType)
    : 'Cliente'

  return {
    role,
    isUser: role === 'user',
    isLawyer,
    professionalType,
    navigation,
    dashboardHome: isLawyer ? '/dashboard/profesional' : '/dashboard/usuario',
    roleLabel: isLawyer ? 'Profesional' : 'Usuario',
    roleDescription,
    isLoading
  }
}
