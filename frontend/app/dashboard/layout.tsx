'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/lib/auth'
import { DashboardLayout } from '@/components/dashboard'

export default function DashboardRootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const router = useRouter()
  const { isAuthenticated, isLoading } = useAuth()

  // Protect all dashboard routes
  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/login')
    }
  }, [isLoading, isAuthenticated, router])

  // Show loading while checking auth
  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-mesh">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-pacific-500"></div>
      </div>
    )
  }

  // Don't render if not authenticated
  if (!isAuthenticated) {
    return null
  }

  return <DashboardLayout>{children}</DashboardLayout>
}
