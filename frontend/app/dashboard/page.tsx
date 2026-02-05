'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/lib/auth'
import { useRole } from '@/lib/hooks/useRole'

export default function DashboardPage() {
  const router = useRouter()
  const { isAuthenticated, isLoading } = useAuth()
  const { dashboardHome } = useRole()

  useEffect(() => {
    if (!isLoading) {
      if (!isAuthenticated) {
        router.push('/login')
      } else {
        // Redirect to role-specific dashboard
        router.push(dashboardHome)
      }
    }
  }, [isLoading, isAuthenticated, dashboardHome, router])

  // Show loading while redirecting
  return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <div className="text-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-pacific-500 mx-auto mb-4"></div>
        <p className="text-slate-500">Cargando dashboard...</p>
      </div>
    </div>
  )
}
