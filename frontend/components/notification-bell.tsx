'use client'

import { useState, useEffect, useRef } from 'react'
import Link from 'next/link'
import { useAuth } from '@/lib/auth'
import { Button } from '@/components/ui/button'
import {
  Bell,
  BellOff,
  Briefcase,
  MessageSquare,
  Phone,
  FileText,
  CheckCircle,
  XCircle,
  X,
  Loader2
} from 'lucide-react'
import { cn } from '@/lib/utils'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface Notification {
  id: number
  type: string
  title: string
  description?: string
  related_case_id?: number
  related_transfer_id?: number
  action_url?: string
  is_read: boolean
  read_at?: string
  created_at: string
}

const typeConfig: Record<string, { icon: React.ElementType; color: string }> = {
  new_case: { icon: Briefcase, color: 'text-blue-500' },
  case_accepted: { icon: CheckCircle, color: 'text-green-500' },
  case_rejected: { icon: XCircle, color: 'text-red-500' },
  new_message: { icon: MessageSquare, color: 'text-pacific-500' },
  call_request: { icon: Phone, color: 'text-purple-500' },
  call_missed: { icon: Phone, color: 'text-orange-500' },
  document_shared: { icon: FileText, color: 'text-slate-500' },
  case_completed: { icon: CheckCircle, color: 'text-green-500' }
}

export function NotificationBell() {
  const { token, isAuthenticated } = useAuth()
  const [notifications, setNotifications] = useState<Notification[]>([])
  const [unreadCount, setUnreadCount] = useState(0)
  const [isOpen, setIsOpen] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)

  const fetchUnreadCount = async () => {
    if (!token) return

    try {
      const response = await fetch(`${API_URL}/api/notifications/unread-count`, {
        headers: { 'Authorization': `Bearer ${token}` }
      })

      if (response.ok) {
        const data = await response.json()
        setUnreadCount(data.unread_count)
      }
    } catch (err) {
      console.error('Error fetching unread count:', err)
    }
  }

  const fetchNotifications = async () => {
    if (!token) return

    setIsLoading(true)

    try {
      const response = await fetch(`${API_URL}/api/notifications/?page_size=10`, {
        headers: { 'Authorization': `Bearer ${token}` }
      })

      if (response.ok) {
        const data = await response.json()
        setNotifications(data.notifications)
        setUnreadCount(data.unread_count)
      }
    } catch (err) {
      console.error('Error fetching notifications:', err)
    } finally {
      setIsLoading(false)
    }
  }

  const markAsRead = async (notificationId: number) => {
    if (!token) return

    try {
      await fetch(`${API_URL}/api/notifications/${notificationId}/read`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      })

      setNotifications(prev =>
        prev.map(n =>
          n.id === notificationId ? { ...n, is_read: true } : n
        )
      )
      setUnreadCount(prev => Math.max(0, prev - 1))
    } catch (err) {
      console.error('Error marking notification as read:', err)
    }
  }

  const markAllAsRead = async () => {
    if (!token) return

    try {
      await fetch(`${API_URL}/api/notifications/read-all`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      })

      setNotifications(prev => prev.map(n => ({ ...n, is_read: true })))
      setUnreadCount(0)
    } catch (err) {
      console.error('Error marking all as read:', err)
    }
  }

  useEffect(() => {
    if (isAuthenticated) {
      fetchUnreadCount()

      // Poll for unread count every 30 seconds
      const interval = setInterval(fetchUnreadCount, 30000)
      return () => clearInterval(interval)
    }
  }, [isAuthenticated, token])

  useEffect(() => {
    if (isOpen) {
      fetchNotifications()
    }
  }, [isOpen])

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const formatRelativeTime = (dateString: string) => {
    const date = new Date(dateString)
    const now = new Date()
    const diffMs = now.getTime() - date.getTime()
    const diffMins = Math.floor(diffMs / 60000)
    const diffHours = Math.floor(diffMins / 60)
    const diffDays = Math.floor(diffHours / 24)

    if (diffMins < 1) return 'Ahora'
    if (diffMins < 60) return `${diffMins}m`
    if (diffHours < 24) return `${diffHours}h`
    if (diffDays < 7) return `${diffDays}d`
    return date.toLocaleDateString('es-CL', { day: 'numeric', month: 'short' })
  }

  if (!isAuthenticated) {
    return null
  }

  return (
    <div className="relative" ref={dropdownRef}>
      <Button
        variant="ghost"
        size="icon"
        onClick={() => setIsOpen(!isOpen)}
        className="relative"
      >
        <Bell className="h-5 w-5 text-slate-600" />
        {unreadCount > 0 && (
          <span className="absolute -top-1 -right-1 flex items-center justify-center h-5 w-5 text-xs font-medium text-white bg-red-500 rounded-full">
            {unreadCount > 9 ? '9+' : unreadCount}
          </span>
        )}
      </Button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-80 bg-white rounded-xl shadow-lg border border-slate-200 overflow-hidden z-50">
          {/* Header */}
          <div className="flex items-center justify-between px-4 py-3 border-b border-slate-200">
            <h3 className="font-semibold text-slate-900">Notificaciones</h3>
            <div className="flex items-center gap-2">
              {unreadCount > 0 && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={markAllAsRead}
                  className="text-xs text-pacific-600 hover:text-pacific-700"
                >
                  Marcar todas leídas
                </Button>
              )}
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setIsOpen(false)}
                className="h-6 w-6"
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
          </div>

          {/* Notifications list */}
          <div className="max-h-96 overflow-y-auto">
            {isLoading ? (
              <div className="flex items-center justify-center py-8">
                <Loader2 className="h-6 w-6 animate-spin text-pacific-500" />
              </div>
            ) : notifications.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-8 text-slate-500">
                <BellOff className="h-8 w-8 mb-2" />
                <p className="text-sm">Sin notificaciones</p>
              </div>
            ) : (
              <div>
                {notifications.map((notification) => {
                  const config = typeConfig[notification.type] || {
                    icon: Bell,
                    color: 'text-slate-500'
                  }
                  const Icon = config.icon

                  const content = (
                    <div
                      className={cn(
                        'flex items-start gap-3 px-4 py-3 hover:bg-slate-50 transition-colors cursor-pointer',
                        !notification.is_read && 'bg-pacific-50'
                      )}
                      onClick={() => {
                        if (!notification.is_read) {
                          markAsRead(notification.id)
                        }
                      }}
                    >
                      <div className={cn('mt-0.5', config.color)}>
                        <Icon className="h-5 w-5" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className={cn(
                          'text-sm',
                          notification.is_read ? 'text-slate-600' : 'text-slate-900 font-medium'
                        )}>
                          {notification.title}
                        </p>
                        {notification.description && (
                          <p className="text-xs text-slate-500 mt-0.5 line-clamp-2">
                            {notification.description}
                          </p>
                        )}
                        <p className="text-xs text-slate-400 mt-1">
                          {formatRelativeTime(notification.created_at)}
                        </p>
                      </div>
                      {!notification.is_read && (
                        <div className="w-2 h-2 rounded-full bg-pacific-500 mt-2" />
                      )}
                    </div>
                  )

                  if (notification.action_url) {
                    return (
                      <Link
                        key={notification.id}
                        href={notification.action_url}
                        onClick={() => setIsOpen(false)}
                      >
                        {content}
                      </Link>
                    )
                  }

                  return <div key={notification.id}>{content}</div>
                })}
              </div>
            )}
          </div>

          {/* Footer */}
          {notifications.length > 0 && (
            <div className="px-4 py-3 border-t border-slate-200">
              <Link
                href="/dashboard/usuario/notificaciones"
                onClick={() => setIsOpen(false)}
                className="text-sm text-pacific-600 hover:text-pacific-700 font-medium"
              >
                Ver todas las notificaciones
              </Link>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
