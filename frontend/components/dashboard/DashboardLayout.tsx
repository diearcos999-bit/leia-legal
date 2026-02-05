'use client'

import { Sidebar } from './Sidebar'
import { MobileSidebar } from './MobileSidebar'

interface DashboardLayoutProps {
  children: React.ReactNode
}

export function DashboardLayout({ children }: DashboardLayoutProps) {
  return (
    <div className="min-h-screen bg-mesh">
      {/* Desktop Sidebar */}
      <Sidebar />

      {/* Mobile Sidebar */}
      <MobileSidebar />

      {/* Main Content */}
      <main className="lg:ml-64 min-h-screen">
        {/* Spacer for mobile header */}
        <div className="lg:hidden h-16" />

        {/* Content */}
        <div className="p-4 lg:p-8">
          {children}
        </div>
      </main>
    </div>
  )
}
