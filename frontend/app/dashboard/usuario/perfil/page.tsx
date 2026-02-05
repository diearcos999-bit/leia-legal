'use client'

import { User, Mail, Shield, Calendar } from 'lucide-react'
import { useAuth } from '@/lib/auth'
import { RoleGuard, PageHeader } from '@/components/dashboard'

export default function PerfilUsuarioPage() {
  const { user } = useAuth()

  return (
    <RoleGuard allowedRole="user">
      <PageHeader
        title="Mi Perfil"
        description="Administra tu informacion personal"
        icon={User}
      />

      <div className="max-w-2xl">
        {/* Profile Card */}
        <div className="glass-card rounded-2xl p-6 mb-6">
          <div className="flex items-center gap-4 mb-6">
            <div className="w-20 h-20 rounded-full bg-pacific-100 flex items-center justify-center">
              <User className="h-10 w-10 text-pacific-600" />
            </div>
            <div>
              <h2 className="text-xl font-semibold text-slate-900">
                {user?.full_name || 'Sin nombre'}
              </h2>
              <p className="text-slate-500">{user?.email}</p>
            </div>
          </div>

          <div className="space-y-4">
            <div className="flex items-center gap-3 p-3 rounded-xl bg-white/50">
              <Mail className="h-5 w-5 text-slate-400" />
              <div>
                <p className="text-sm text-slate-500">Correo electronico</p>
                <p className="font-medium text-slate-900">{user?.email}</p>
              </div>
            </div>

            <div className="flex items-center gap-3 p-3 rounded-xl bg-white/50">
              <Shield className="h-5 w-5 text-slate-400" />
              <div>
                <p className="text-sm text-slate-500">Estado de verificacion</p>
                <p className={`font-medium ${user?.is_verified ? 'text-green-600' : 'text-amber-600'}`}>
                  {user?.is_verified ? 'Verificado' : 'Pendiente de verificacion'}
                </p>
              </div>
            </div>

            <div className="flex items-center gap-3 p-3 rounded-xl bg-white/50">
              <Calendar className="h-5 w-5 text-slate-400" />
              <div>
                <p className="text-sm text-slate-500">Miembro desde</p>
                <p className="font-medium text-slate-900">
                  {user?.created_at
                    ? new Date(user.created_at).toLocaleDateString('es-CL', {
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric'
                      })
                    : 'N/A'}
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Account Settings */}
        <div className="glass-card rounded-2xl p-6">
          <h3 className="text-lg font-semibold text-slate-900 mb-4">
            Configuracion de Cuenta
          </h3>
          <p className="text-sm text-slate-500">
            La edición de perfil estara disponible proximamente.
          </p>
        </div>
      </div>
    </RoleGuard>
  )
}
