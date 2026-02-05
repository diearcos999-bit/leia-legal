'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Menu, X, LogOut } from 'lucide-react'
import { LeiaLogo } from '@/components/ui/leia-logo'
import { Button } from '@/components/ui/button'
import { useAuth } from '@/lib/auth'
import { useRole } from '@/lib/hooks/useRole'
import { SidebarNav } from './SidebarNav'
import { SidebarUserInfo } from './SidebarUserInfo'
import { NotificationBell } from '@/components/notification-bell'
import { cn } from '@/lib/utils'

export function MobileSidebar() {
  const [isOpen, setIsOpen] = useState(false)
  const { logout } = useAuth()
  const { dashboardHome } = useRole()
  const pathname = usePathname()

  // Close sidebar on route change
  useEffect(() => {
    setIsOpen(false)
  }, [pathname])

  // Prevent body scroll when sidebar is open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = ''
    }
    return () => {
      document.body.style.overflow = ''
    }
  }, [isOpen])

  return (
    <>
      {/* Mobile Header */}
      <header className="lg:hidden fixed top-0 left-0 right-0 z-50 h-16 glass-heavy border-b border-white/20 flex items-center justify-between px-4">
        <Link href={dashboardHome}>
          <LeiaLogo size="sm" />
        </Link>
        <div className="flex items-center gap-2">
          <NotificationBell />
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="p-2 rounded-xl hover:bg-white/50 transition-colors"
            aria-label={isOpen ? 'Cerrar menu' : 'Abrir menu'}
          >
            {isOpen ? (
              <X className="h-6 w-6 text-slate-700" />
            ) : (
              <Menu className="h-6 w-6 text-slate-700" />
            )}
          </button>
        </div>
      </header>

      {/* Backdrop */}
      <div
        className={cn(
          'lg:hidden fixed inset-0 z-40 bg-black/20 backdrop-blur-sm transition-opacity duration-300',
          isOpen ? 'opacity-100' : 'opacity-0 pointer-events-none'
        )}
        onClick={() => setIsOpen(false)}
      />

      {/* Sidebar Drawer */}
      <aside
        className={cn(
          'lg:hidden fixed top-0 left-0 z-50 h-screen w-72 glass-heavy border-r border-white/20 flex flex-col transition-transform duration-300 ease-out',
          isOpen ? 'translate-x-0' : '-translate-x-full'
        )}
      >
        {/* Logo */}
        <div className="h-16 flex items-center justify-between px-6 border-b border-white/10">
          <Link href={dashboardHome} onClick={() => setIsOpen(false)}>
            <LeiaLogo size="md" />
          </Link>
          <button
            onClick={() => setIsOpen(false)}
            className="p-2 rounded-xl hover:bg-white/50 transition-colors"
            aria-label="Cerrar menu"
          >
            <X className="h-5 w-5 text-slate-600" />
          </button>
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
            onClick={() => {
              setIsOpen(false)
              logout()
            }}
          >
            <LogOut className="h-4 w-4 mr-3" />
            Cerrar Sesion
          </Button>
        </div>
      </aside>
    </>
  )
}
