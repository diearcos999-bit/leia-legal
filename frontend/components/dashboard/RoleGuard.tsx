'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/lib/auth'
import { useRole, type UserRole } from '@/lib/hooks/useRole'

interface RoleGuardProps {
  children: React.ReactNode
  allowedRole: UserRole
  fallbackPath?: string
}

export function RoleGuard({ children, allowedRole, fallbackPath }: RoleGuardProps) {
  const router = useRouter()
  const { isAuthenticated, isLoading } = useAuth()
  const { role, dashboardHome } = useRole()

  useEffect(() => {
    if (!isLoading) {
      if (!isAuthenticated) {
        router.push('/login')
      } else if (role !== allowedRole) {
        // Redirect to appropriate dashboard
        router.push(fallbackPath || dashboardHome)
      }
    }
  }, [isLoading, isAuthenticated, role, allowedRole, fallbackPath, dashboardHome, router])

  // Show loading while checking auth
  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-pacific-500"></div>
      </div>
    )
  }

  // Don't render if not authenticated or wrong role
  if (!isAuthenticated || role !== allowedRole) {
    return null
  }

  return <>{children}</>
}
