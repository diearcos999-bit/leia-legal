'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Header } from '@/components/layout/Header'
import { LeiaAvatar } from '@/components/ui/leia-avatar'
import { AlertCircle, ArrowRight, User, Briefcase } from 'lucide-react'
import { useAuth } from '@/lib/auth'
import { cn } from '@/lib/utils'

type LoginType = 'user' | 'professional'

export default function LoginPage() {
  const router = useRouter()
  const { loginWithCredentials, isAuthenticated, isLoading: authLoading, user, professionalType } = useAuth()
  const [loginType, setLoginType] = useState<LoginType>('user')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!authLoading && isAuthenticated && user) {
      // Redirect based on user role
      if (user.role === 'lawyer') {
        router.push('/dashboard/profesional')
      } else {
        router.push('/dashboard/usuario')
      }
    }
  }, [authLoading, isAuthenticated, user, router])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError(null)

    const result = await loginWithCredentials({ email, password })

    if (result.success) {
      // Redirect will happen in useEffect when user state updates
    } else {
      setError(result.error || 'Error al iniciar sesion')
      setIsLoading(false)
    }
  }

  if (authLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-mesh">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-pacific-600"></div>
      </div>
    )
  }

  const isUser = loginType === 'user'

  return (
    <div className="flex flex-col min-h-screen bg-mesh">
      <Header />

      <section className="relative pt-28 lg:pt-36 pb-16 flex-1 flex items-center">
        <div className={cn(
          "absolute top-20 left-1/4 w-96 h-96 rounded-full blur-3xl animate-pulse-glow transition-colors duration-500",
          isUser ? "bg-pacific-400/20" : "bg-terracota-400/20"
        )} />
        <div className={cn(
          "absolute bottom-0 right-1/4 w-80 h-80 rounded-full blur-3xl animate-pulse-glow transition-colors duration-500",
          isUser ? "bg-terracota-400/10" : "bg-pacific-400/10"
        )} style={{ animationDelay: '1s' }} />

        <div className="container relative">
          <div className="max-w-md mx-auto">
            <div className="glass-panel rounded-3xl p-8">
              {/* Tabs */}
              <div className="flex mb-6 p-1 bg-slate-100/80 rounded-2xl">
                <button
                  type="button"
                  onClick={() => setLoginType('user')}
                  className={cn(
                    "flex-1 flex items-center justify-center gap-2 py-3 px-4 rounded-xl text-sm font-medium transition-all duration-300",
                    isUser
                      ? "bg-white text-pacific-700 shadow-md"
                      : "text-slate-500 hover:text-slate-700"
                  )}
                >
                  <User className="h-4 w-4" />
                  Usuario
                </button>
                <button
                  type="button"
                  onClick={() => setLoginType('professional')}
                  className={cn(
                    "flex-1 flex items-center justify-center gap-2 py-3 px-4 rounded-xl text-sm font-medium transition-all duration-300",
                    !isUser
                      ? "bg-white text-terracota-700 shadow-md"
                      : "text-slate-500 hover:text-slate-700"
                  )}
                >
                  <Briefcase className="h-4 w-4" />
                  Profesional
                </button>
              </div>

              <div className="text-center mb-8">
                <div className="flex justify-center mb-4">
                  <LeiaAvatar size="md" />
                </div>
                <h1 className="text-2xl font-semibold text-slate-900 mb-2">
                  {isUser ? 'Bienvenido de vuelta' : 'Portal Profesional'}
                </h1>
                <p className="text-slate-600">
                  {isUser
                    ? 'Ingresa a tu cuenta de LEIA'
                    : 'Accede a tu panel de abogado'}
                </p>
              </div>

              <form onSubmit={handleSubmit} className="space-y-4">
                {error && (
                  <div className="flex items-center gap-2 p-3 text-sm text-red-600 bg-red-50 border border-red-200 rounded-xl">
                    <AlertCircle className="h-4 w-4 flex-shrink-0" />
                    <span>{error}</span>
                  </div>
                )}

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">
                    Correo electrónico
                  </label>
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    className={cn(
                      "w-full px-4 py-3 rounded-xl glass-input text-slate-800 placeholder:text-slate-400 focus:outline-none transition-all duration-300",
                      !isUser && "focus:ring-2 focus:ring-terracota-500/20 focus:border-terracota-500"
                    )}
                    placeholder={isUser ? "tu@correo.cl" : "abogado@correo.cl"}
                  />
                </div>

                <div>
                  <div className="flex items-center justify-between mb-1">
                    <label className="block text-sm font-medium text-slate-700">
                      Contraseña
                    </label>
                    <Link href="/recuperar" className={cn(
                      "text-sm hover:underline transition-colors",
                      isUser ? "text-pacific-600" : "text-terracota-600"
                    )}>
                      ¿Olvidaste tu contraseña?
                    </Link>
                  </div>
                  <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    className={cn(
                      "w-full px-4 py-3 rounded-xl glass-input text-slate-800 placeholder:text-slate-400 focus:outline-none transition-all duration-300",
                      !isUser && "focus:ring-2 focus:ring-terracota-500/20 focus:border-terracota-500"
                    )}
                    placeholder="••••••••"
                  />
                </div>

                <div className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    id="remember"
                    className="h-4 w-4 rounded border-slate-300"
                  />
                  <label htmlFor="remember" className="text-sm text-slate-600">
                    Recordarme
                  </label>
                </div>

                <Button
                  type="submit"
                  variant={isUser ? "pacific" : "default"}
                  size="lg"
                  className={cn(
                    "w-full mt-6 transition-all duration-300",
                    !isUser && "bg-gradient-to-b from-terracota-500 to-terracota-600 hover:from-terracota-400 hover:to-terracota-500 shadow-lg shadow-terracota-500/25"
                  )}
                  disabled={isLoading}
                >
                  {isLoading ? 'Ingresando...' : 'Ingresar'}
                  {!isLoading && <ArrowRight className="ml-2 h-5 w-5" />}
                </Button>

                {isUser && (
                  <>
                    <div className="relative my-6">
                      <div className="absolute inset-0 flex items-center">
                        <div className="w-full border-t border-slate-200"></div>
                      </div>
                      <div className="relative flex justify-center text-sm">
                        <span className="px-2 bg-white/80 text-slate-500">o continúa con</span>
                      </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                      <Button type="button" variant="outline" className="w-full">
                        <svg className="h-5 w-5 mr-2" viewBox="0 0 24 24">
                          <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                          <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                          <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                          <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                        </svg>
                        Google
                      </Button>
                      <Button type="button" variant="outline" className="w-full">
                        <svg className="h-5 w-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
                          <path d="M12 2C6.477 2 2 6.477 2 12c0 4.42 2.865 8.164 6.839 9.489.5.092.682-.217.682-.482 0-.237-.008-.866-.013-1.7-2.782.604-3.369-1.341-3.369-1.341-.454-1.155-1.11-1.462-1.11-1.462-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.087 2.91.831.092-.646.35-1.086.636-1.336-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.269 2.75 1.025A9.578 9.578 0 0112 6.836c.85.004 1.705.114 2.504.336 1.909-1.294 2.747-1.025 2.747-1.025.546 1.377.203 2.394.1 2.647.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.578.688.48C19.138 20.161 22 16.418 22 12c0-5.523-4.477-10-10-10z"/>
                        </svg>
                        GitHub
                      </Button>
                    </div>
                  </>
                )}
              </form>

              <p className="text-center text-sm text-slate-500 mt-6">
                {isUser ? (
                  <>
                    ¿No tienes cuenta?{" "}
                    <Link href="/registro" className="text-pacific-600 hover:underline">
                      Regístrate gratis
                    </Link>
                  </>
                ) : (
                  <>
                    ¿Aún no eres parte de LEIA?{" "}
                    <Link href="/unirse" className="text-terracota-600 hover:underline">
                      Únete como profesional
                    </Link>
                  </>
                )}
              </p>

              {isUser && (
                <p className="text-center text-sm text-slate-500 mt-4">
                  ¿Eres abogado?{" "}
                  <button
                    type="button"
                    onClick={() => setLoginType('professional')}
                    className="text-terracota-600 hover:underline"
                  >
                    Ingresa como profesional
                  </button>
                </p>
              )}
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 border-t border-slate-200/50">
        <div className="container">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-sm text-slate-500 flex items-center gap-2">
              © 2025 LEIA. Hecho en Chile
              <svg viewBox="0 0 30 20" className="h-4 w-6 rounded shadow-sm" aria-label="Chile">
                <rect x="0" y="0" width="10" height="10" fill="#0039A6" />
                <polygon points="5,2 6.2,5.5 9.5,5.5 6.8,7.5 7.8,11 5,8.5 2.2,11 3.2,7.5 0.5,5.5 3.8,5.5" fill="white" transform="scale(0.7) translate(2.1, 1.4)" />
                <rect x="10" y="0" width="20" height="10" fill="white" />
                <rect x="0" y="10" width="30" height="10" fill="#D52B1E" />
              </svg>
            </p>
            <div className="flex gap-6 text-sm">
              <Link href="/terminos" className="text-slate-600 hover:text-slate-900 transition-colors">Términos</Link>
              <Link href="/privacidad" className="text-slate-600 hover:text-slate-900 transition-colors">Privacidad</Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
