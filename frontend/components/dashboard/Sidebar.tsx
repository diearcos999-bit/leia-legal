'use client'

import Link from 'next/link'
import { LogOut } from 'lucide-react'
import { LeiaLogo } from '@/components/ui/leia-logo'
import { Button } from '@/components/ui/button'
import { useAuth } from '@/lib/auth'
import { useRole } from '@/lib/hooks/useRole'
import { SidebarNav } from './SidebarNav'
import { SidebarUserInfo } from './SidebarUserInfo'
import { NotificationBell } from '@/components/notification-bell'

export function Sidebar() {
  const { logout } = useAuth()
  const { dashboardHome } = useRole()

  return (
    <aside className="fixed left-0 top-0 z-40 h-screen w-64 glass-heavy border-r border-white/20 hidden lg:flex flex-col">
      {/* Logo and Notifications */}
      <div className="h-16 flex items-center justify-between px-6 border-b border-white/10">
        <Link href={dashboardHome}>
          <LeiaLogo size="md" />
        </Link>
        <NotificationBell />
      </div>

      {/* User Info */}
      <SidebarUserInfo />

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto py-4 px-3">
        <SidebarNav />
      </nav>

      {/* Logout */}
      <div className="p-4 border-t border-white/10">
        <Button
          variant="ghost"
          className="w-full justify-start text-slate-600 hover:text-slate-900 hover:bg-white/50"
          onClick={logout}
        >
          <LogOut className="h-4 w-4 mr-3" />
          Cerrar Sesion
        </Button>
      </div>
    </aside>
  )
}
