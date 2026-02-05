'use client'

import { CalendarDays, ChevronLeft, ChevronRight } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { RoleGuard, PageHeader } from '@/components/dashboard'

export default function CalendarioPage() {
  const today = new Date()
  const monthName = today.toLocaleDateString('es-CL', { month: 'long', year: 'numeric' })

  return (
    <RoleGuard allowedRole="lawyer">
      <PageHeader
        title="Calendario"
        description="Gestiona tu agenda y citas"
        icon={CalendarDays}
      />

      <div className="glass-card rounded-2xl p-6">
        {/* Calendar Header */}
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-lg font-semibold text-slate-900 capitalize">
            {monthName}
          </h2>
          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm" disabled>
              <ChevronLeft className="h-4 w-4" />
            </Button>
            <Button variant="outline" size="sm" disabled>
              Hoy
            </Button>
            <Button variant="outline" size="sm" disabled>
              <ChevronRight className="h-4 w-4" />
            </Button>
          </div>
        </div>

        {/* Calendar Grid Placeholder */}
        <div className="border border-slate-200 rounded-xl overflow-hidden">
          {/* Days Header */}
          <div className="grid grid-cols-7 bg-slate-50">
            {['Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab', 'Dom'].map((day) => (
              <div key={day} className="p-3 text-center text-sm font-medium text-slate-600 border-b border-slate-200">
                {day}
              </div>
            ))}
          </div>

          {/* Calendar Days Placeholder */}
          <div className="grid grid-cols-7">
            {Array.from({ length: 35 }, (_, i) => {
              const dayNum = i - 3 // Offset for month start
              const isToday = dayNum === today.getDate()
              const isCurrentMonth = dayNum > 0 && dayNum <= 31

              return (
                <div
                  key={i}
                  className={`min-h-[80px] p-2 border-b border-r border-slate-100 ${
                    !isCurrentMonth ? 'bg-slate-50/50' : ''
                  }`}
                >
                  {isCurrentMonth && (
                    <span className={`inline-flex items-center justify-center w-7 h-7 rounded-full text-sm ${
                      isToday
                        ? 'bg-pacific-500 text-white font-semibold'
                        : 'text-slate-600'
                    }`}>
                      {dayNum}
                    </span>
                  )}
                </div>
              )
            })}
          </div>
        </div>

        <p className="text-sm text-slate-500 mt-4 text-center">
          El calendario interactivo estara disponible proximamente.
        </p>
      </div>
    </RoleGuard>
  )
}
