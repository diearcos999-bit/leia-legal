'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { X, Mail, Lock, User, Phone, Loader2, AlertCircle, CreditCard } from 'lucide-react'

// Validación de RUT chileno
function validateRut(rut: string): boolean {
  // Limpiar el RUT
  const cleanRut = rut.toUpperCase().replace(/\./g, '').replace(/-/g, '').replace(/\s/g, '')

  if (cleanRut.length < 8 || cleanRut.length > 9) return false

  const cuerpo = cleanRut.slice(0, -1)
  const dv = cleanRut.slice(-1)

  if (!/^\d+$/.test(cuerpo)) return false

  // Calcular dígito verificador
  let suma = 0
  let multiplo = 2

  for (let i = cuerpo.length - 1; i >= 0; i--) {
    suma += parseInt(cuerpo[i]) * multiplo
    multiplo = multiplo < 7 ? multiplo + 1 : 2
  }

  const resto = suma % 11
  const dvCalculado = 11 - resto

  let dvEsperado: string
  if (dvCalculado === 11) dvEsperado = '0'
  else if (dvCalculado === 10) dvEsperado = 'K'
  else dvEsperado = dvCalculado.toString()

  return dv === dvEsperado
}

// Formatear RUT mientras se escribe
function formatRut(value: string): string {
  const cleaned = value.replace(/[^0-9kK]/g, '').toUpperCase()
  if (cleaned.length <= 1) return cleaned

  const cuerpo = cleaned.slice(0, -1)
  const dv = cleaned.slice(-1)

  // Agregar puntos
  let formatted = ''
  for (let i = cuerpo.length - 1, count = 0; i >= 0; i--, count++) {
    if (count > 0 && count % 3 === 0) formatted = '.' + formatted
    formatted = cuerpo[i] + formatted
  }

  return `${formatted}-${dv}`
}

interface AuthModalProps {
  isOpen: boolean
  onClose: () => void
  onSuccess: () => void
  login: (data: { email: string; password: string }) => Promise<{ success: boolean; error?: string }>
  register: (data: { email: string; password: string; full_name: string; phone: string; rut: string }) => Promise<{ success: boolean; error?: string }>
  mode?: 'login' | 'register'
  reason?: 'limit' | 'lawyer' | 'general'
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export function AuthModal({
  isOpen,
  onClose,
  onSuccess,
  login,
  register,
  mode: initialMode = 'register',
  reason = 'general'
}: AuthModalProps) {
  const [mode, setMode] = useState<'login' | 'register'>(initialMode)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Form fields
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [fullName, setFullName] = useState('')
  const [phone, setPhone] = useState('')
  const [rut, setRut] = useState('')
  const [rutError, setRutError] = useState<string | null>(null)

  // Handle RUT input with formatting
  const handleRutChange = (value: string) => {
    const formatted = formatRut(value)
    setRut(formatted)

    // Validar solo si tiene longitud suficiente
    if (value.replace(/[^0-9kK]/g, '').length >= 8) {
      if (!validateRut(formatted)) {
        setRutError('RUT inválido')
      } else {
        setRutError(null)
      }
    } else {
      setRutError(null)
    }
  }

  if (!isOpen) return null

  const reasonMessages = {
    limit: {
      title: 'Crea tu cuenta',
      subtitle: 'Regístrate para seguir consultando con LEIA sin límites. Es rápido y sencillo.'
    },
    lawyer: {
      title: 'Registrate para contactar abogados',
      subtitle: 'Necesitas una cuenta para enviar tu caso a un abogado y recibir respuesta.'
    },
    general: {
      title: mode === 'login' ? 'Inicia sesión' : 'Crea tu cuenta',
      subtitle: mode === 'login'
        ? 'Accede a tu cuenta para continuar'
        : 'Regístrate para guardar tu historial y contactar abogados'
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setIsLoading(true)

    try {
      let result
      if (mode === 'login') {
        result = await login({ email, password })
      } else {
        // Validar campos requeridos
        if (!fullName.trim()) {
          setError('El nombre es requerido')
          setIsLoading(false)
          return
        }
        if (!rut.trim()) {
          setError('El RUT es requerido')
          setIsLoading(false)
          return
        }
        if (!validateRut(rut)) {
          setError('El RUT ingresado no es válido')
          setIsLoading(false)
          return
        }
        if (!phone.trim()) {
          setError('El teléfono es requerido')
          setIsLoading(false)
          return
        }

        result = await register({
          email,
          password,
          full_name: fullName,
          phone: phone,
          rut: rut
        })
      }

      if (result.success) {
        onSuccess()
        onClose()
      } else {
        setError(result.error || 'Error desconocido')
      }
    } catch {
      setError('Error de conexion')
    } finally {
      setIsLoading(false)
    }
  }

  const handleSocialLogin = (provider: string) => {
    // Redirigir al backend para OAuth
    window.location.href = `${API_URL}/api/auth/oauth/${provider}`
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="relative bg-white rounded-2xl shadow-2xl w-full max-w-md mx-4 overflow-hidden animate-fade-in-up max-h-[90vh] overflow-y-auto">
        {/* Close button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-2 rounded-full hover:bg-slate-100 transition-colors z-10"
        >
          <X className="h-5 w-5 text-slate-500" />
        </button>

        {/* Header */}
        <div className="px-8 pt-8 pb-4 text-center">
          <h2 className="text-2xl font-semibold text-slate-900 mb-2">
            {reasonMessages[reason].title}
          </h2>
          <p className="text-slate-600 text-sm">
            {reasonMessages[reason].subtitle}
          </p>
        </div>

        {/* Social Login Buttons */}
        <div className="px-8 pb-4">
          <div className="grid grid-cols-2 gap-3">
            {/* Google */}
            <button
              type="button"
              onClick={() => handleSocialLogin('google')}
              className="flex items-center justify-center gap-2 px-4 py-3 rounded-xl border border-slate-200 hover:bg-slate-50 transition-colors"
            >
              <svg className="h-5 w-5" viewBox="0 0 24 24">
                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
              </svg>
              <span className="text-sm font-medium text-slate-700">Google</span>
            </button>

            {/* Facebook */}
            <button
              type="button"
              onClick={() => handleSocialLogin('facebook')}
              className="flex items-center justify-center gap-2 px-4 py-3 rounded-xl border border-slate-200 hover:bg-slate-50 transition-colors"
            >
              <svg className="h-5 w-5" viewBox="0 0 24 24" fill="#1877F2">
                <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
              </svg>
              <span className="text-sm font-medium text-slate-700">Facebook</span>
            </button>

            {/* LinkedIn */}
            <button
              type="button"
              onClick={() => handleSocialLogin('linkedin')}
              className="flex items-center justify-center gap-2 px-4 py-3 rounded-xl border border-slate-200 hover:bg-slate-50 transition-colors"
            >
              <svg className="h-5 w-5" viewBox="0 0 24 24" fill="#0A66C2">
                <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
              </svg>
              <span className="text-sm font-medium text-slate-700">LinkedIn</span>
            </button>

            {/* Apple */}
            <button
              type="button"
              onClick={() => handleSocialLogin('apple')}
              className="flex items-center justify-center gap-2 px-4 py-3 rounded-xl border border-slate-200 hover:bg-slate-50 transition-colors"
            >
              <svg className="h-5 w-5" viewBox="0 0 24 24" fill="#000000">
                <path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z"/>
              </svg>
              <span className="text-sm font-medium text-slate-700">Apple</span>
            </button>
          </div>

          {/* Divider */}
          <div className="relative my-6">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-slate-200"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-4 bg-white text-slate-500">o continua con email</span>
            </div>
          </div>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="px-8 pb-8">
          {/* Error message */}
          {error && (
            <div className="mb-4 p-3 rounded-lg bg-red-50 border border-red-200 flex items-center gap-2">
              <AlertCircle className="h-4 w-4 text-red-500 flex-shrink-0" />
              <p className="text-sm text-red-600">{error}</p>
            </div>
          )}

          {/* Name field (required for register) */}
          {mode === 'register' && (
            <div className="mb-4">
              <label className="block text-sm font-medium text-slate-700 mb-1">
                Nombre completo <span className="text-red-500">*</span>
              </label>
              <div className="relative">
                <User className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-slate-400" />
                <input
                  type="text"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  placeholder="Tu nombre completo"
                  required
                  className="w-full pl-10 pr-4 py-3 rounded-xl border border-slate-200 focus:border-pacific-500 focus:ring-2 focus:ring-pacific-500/20 outline-none transition-all"
                />
              </div>
            </div>
          )}

          {/* RUT field (required for register) */}
          {mode === 'register' && (
            <div className="mb-4">
              <label className="block text-sm font-medium text-slate-700 mb-1">
                RUT <span className="text-red-500">*</span>
              </label>
              <div className="relative">
                <CreditCard className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-slate-400" />
                <input
                  type="text"
                  value={rut}
                  onChange={(e) => handleRutChange(e.target.value)}
                  placeholder="12.345.678-9"
                  required
                  maxLength={12}
                  className={`w-full pl-10 pr-4 py-3 rounded-xl border ${
                    rutError ? 'border-red-300 focus:border-red-500 focus:ring-red-500/20' : 'border-slate-200 focus:border-pacific-500 focus:ring-pacific-500/20'
                  } outline-none transition-all`}
                />
              </div>
              {rutError && (
                <p className="text-xs text-red-500 mt-1">{rutError}</p>
              )}
            </div>
          )}

          {/* Email field */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-slate-700 mb-1">
              Email <span className="text-red-500">*</span>
            </label>
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-slate-400" />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="tu@email.com"
                required
                className="w-full pl-10 pr-4 py-3 rounded-xl border border-slate-200 focus:border-pacific-500 focus:ring-2 focus:ring-pacific-500/20 outline-none transition-all"
              />
            </div>
          </div>

          {/* Password field */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-slate-700 mb-1">
              Contraseña <span className="text-red-500">*</span>
            </label>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-slate-400" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                required
                minLength={8}
                className="w-full pl-10 pr-4 py-3 rounded-xl border border-slate-200 focus:border-pacific-500 focus:ring-2 focus:ring-pacific-500/20 outline-none transition-all"
              />
            </div>
            {mode === 'register' && (
              <p className="text-xs text-slate-500 mt-1">Mínimo 8 caracteres, con letras y números</p>
            )}
          </div>

          {/* Phone field (required for register) */}
          {mode === 'register' && (
            <div className="mb-6">
              <label className="block text-sm font-medium text-slate-700 mb-1">
                Telefono <span className="text-red-500">*</span>
              </label>
              <div className="relative">
                <Phone className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-slate-400" />
                <input
                  type="tel"
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  placeholder="+56 9 1234 5678"
                  required
                  className="w-full pl-10 pr-4 py-3 rounded-xl border border-slate-200 focus:border-pacific-500 focus:ring-2 focus:ring-pacific-500/20 outline-none transition-all"
                />
              </div>
              <p className="text-xs text-slate-500 mt-1">
                Para que los abogados puedan contactarte
              </p>
            </div>
          )}

          {/* Submit button */}
          <Button
            type="submit"
            variant="pacific"
            className="w-full py-3 text-base"
            disabled={isLoading}
          >
            {isLoading ? (
              <>
                <Loader2 className="h-5 w-5 animate-spin mr-2" />
                {mode === 'login' ? 'Iniciando sesion...' : 'Registrando...'}
              </>
            ) : (
              mode === 'login' ? 'Iniciar sesión' : 'Crear cuenta'
            )}
          </Button>

          {/* Toggle mode */}
          <div className="mt-6 text-center">
            <p className="text-sm text-slate-600">
              {mode === 'login' ? '¿No tienes cuenta?' : '¿Ya tienes cuenta?'}
              <button
                type="button"
                onClick={() => {
                  setMode(mode === 'login' ? 'register' : 'login')
                  setError(null)
                }}
                className="ml-1 text-pacific-600 font-medium hover:underline"
              >
                {mode === 'login' ? 'Registrate' : 'Inicia sesion'}
              </button>
            </p>
          </div>
        </form>

        {/* Footer */}
        <div className="px-8 py-4 bg-slate-50 border-t border-slate-100">
          <p className="text-xs text-slate-500 text-center">
            Al continuar, aceptas nuestros{' '}
            <a href="/terminos" className="text-pacific-600 hover:underline">Terminos</a>
            {' '}y{' '}
            <a href="/privacidad" className="text-pacific-600 hover:underline">Politica de Privacidad</a>
          </p>
        </div>
      </div>
    </div>
  )
}
