"use client"

import * as React from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { X, ArrowRight, Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import { useAuth } from "@/lib/auth"

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface RegistrationModalProps {
  isOpen: boolean
  onClose: () => void
  type: "usuario" | "profesional"
  plan?: string
}

interface FormData {
  firstName: string
  lastName: string
  email: string
  password: string
  phone: string
  professionalType: string
  specialty: string
  acceptTerms: boolean
}

export function RegistrationModal({ isOpen, onClose, type, plan }: RegistrationModalProps) {
  const [isClosing, setIsClosing] = React.useState(false)
  const [isLoading, setIsLoading] = React.useState(false)
  const [error, setError] = React.useState<string | null>(null)
  const router = useRouter()
  const { login } = useAuth()

  const [formData, setFormData] = React.useState<FormData>({
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    phone: '',
    professionalType: '',
    specialty: '',
    acceptTerms: false
  })

  const handleClose = () => {
    setIsClosing(true)
    setTimeout(() => {
      setIsClosing(false)
      setError(null)
      onClose()
    }, 200)
  }

  // Close on escape key
  React.useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === "Escape") handleClose()
    }
    if (isOpen) {
      document.addEventListener("keydown", handleEscape)
      document.body.style.overflow = "hidden"
    }
    return () => {
      document.removeEventListener("keydown", handleEscape)
      document.body.style.overflow = "unset"
    }
  }, [isOpen])

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type: inputType } = e.target
    const newValue = inputType === 'checkbox' ? (e.target as HTMLInputElement).checked : value
    setFormData(prev => ({ ...prev, [name]: newValue }))
    setError(null)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setIsLoading(true)

    // Validation
    if (!formData.acceptTerms) {
      setError('Debes aceptar los términos y condiciones')
      setIsLoading(false)
      return
    }

    try {
      if (type === "profesional") {
        // Professional registration
        if (!formData.professionalType) {
          setError('Selecciona el tipo de profesional')
          setIsLoading(false)
          return
        }
        if (!formData.specialty) {
          setError('Selecciona tu área de especialización')
          setIsLoading(false)
          return
        }

        const response = await fetch(`${API_URL}/api/auth/register/professional`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            email: formData.email,
            password: formData.password,
            full_name: `${formData.firstName} ${formData.lastName}`.trim(),
            professional_type: formData.professionalType,
            specialty: formData.specialty,
            phone: formData.phone || null
          })
        })

        const data = await response.json()

        if (!response.ok) {
          throw new Error(data.detail || 'Error al registrar')
        }

        // Login with the returned token and professional type
        login(data.access_token, data.user, data.professional_type, data.lawyer_id)

        // Redirect based on professional type
        handleClose()
        router.push('/dashboard/profesional')
      } else {
        // Regular user registration
        const response = await fetch(`${API_URL}/api/auth/register`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            email: formData.email,
            password: formData.password,
            full_name: `${formData.firstName} ${formData.lastName}`.trim()
          })
        })

        const data = await response.json()

        if (!response.ok) {
          throw new Error(data.detail || 'Error al registrar')
        }

        // Login with the returned token
        login(data.access_token, data.user)

        // Redirect to user dashboard
        handleClose()
        router.push('/dashboard/usuario')
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error al registrar')
    } finally {
      setIsLoading(false)
    }
  }

  if (!isOpen) return null

  return (
    <div
      className={cn(
        "fixed inset-0 z-50 flex items-center justify-center p-4",
        "transition-opacity duration-200",
        isClosing ? "opacity-0" : "opacity-100"
      )}
    >
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-slate-900/60 backdrop-blur-sm"
        onClick={handleClose}
      />

      {/* Modal */}
      <div
        className={cn(
          "relative w-full max-w-md max-h-[90vh] overflow-y-auto",
          "glass-panel rounded-3xl p-8",
          "transform transition-all duration-200",
          isClosing ? "scale-95 opacity-0" : "scale-100 opacity-100"
        )}
      >
        {/* Close button */}
        <button
          onClick={handleClose}
          className="absolute top-4 right-4 p-2 rounded-xl text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition-colors"
        >
          <X className="h-5 w-5" />
        </button>

        {/* Content */}
        <div className="text-center mb-6">
          <h2 className="text-2xl font-semibold text-slate-900 mb-2">
            {type === "profesional" ? "Crea tu perfil profesional" : "Crea tu cuenta"}
          </h2>
          <p className="text-slate-600 text-sm">
            {type === "profesional"
              ? "Unete a la red de profesionales legales de Chile"
              : "Accede a orientacion legal con inteligencia artificial"}
          </p>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                Nombre
              </label>
              <input
                type="text"
                name="firstName"
                value={formData.firstName}
                onChange={handleInputChange}
                className="w-full px-4 py-2.5 rounded-xl glass-input text-slate-800 placeholder:text-slate-400 focus:outline-none text-sm"
                placeholder="Juan"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                Apellido
              </label>
              <input
                type="text"
                name="lastName"
                value={formData.lastName}
                onChange={handleInputChange}
                className="w-full px-4 py-2.5 rounded-xl glass-input text-slate-800 placeholder:text-slate-400 focus:outline-none text-sm"
                placeholder="Perez"
                required
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              Correo electronico
            </label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleInputChange}
              className="w-full px-4 py-2.5 rounded-xl glass-input text-slate-800 placeholder:text-slate-400 focus:outline-none text-sm"
              placeholder="juan@ejemplo.cl"
              required
            />
          </div>

          {type === "profesional" && (
            <>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  Telefono
                </label>
                <input
                  type="tel"
                  name="phone"
                  value={formData.phone}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2.5 rounded-xl glass-input text-slate-800 placeholder:text-slate-400 focus:outline-none text-sm"
                  placeholder="+56 9 1234 5678"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  Tipo de profesional
                </label>
                <select
                  name="professionalType"
                  value={formData.professionalType}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2.5 rounded-xl glass-input text-slate-800 focus:outline-none text-sm"
                  required
                >
                  <option value="">Selecciona una opcion</option>
                  <option value="abogado">Abogado/a</option>
                  <option value="procurador">Procurador/a</option>
                  <option value="estudio">Estudio Juridico</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  Area principal
                </label>
                <select
                  name="specialty"
                  value={formData.specialty}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2.5 rounded-xl glass-input text-slate-800 focus:outline-none text-sm"
                  required
                >
                  <option value="">Selecciona tu especializacion</option>
                  <option value="Derecho Laboral">Derecho Laboral</option>
                  <option value="Derecho de Familia">Derecho de Familia</option>
                  <option value="Derecho Civil">Derecho Civil</option>
                  <option value="Derecho Penal">Derecho Penal</option>
                  <option value="Derecho Comercial">Derecho Comercial</option>
                  <option value="Derecho Tributario">Derecho Tributario</option>
                  <option value="Derecho Inmobiliario">Derecho Inmobiliario</option>
                  <option value="Derecho del Consumidor">Derecho del Consumidor</option>
                </select>
              </div>
            </>
          )}

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              Contrasena
            </label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleInputChange}
              className="w-full px-4 py-2.5 rounded-xl glass-input text-slate-800 placeholder:text-slate-400 focus:outline-none text-sm"
              placeholder="Minimo 8 caracteres"
              minLength={8}
              required
            />
          </div>

          <div className="flex items-start gap-2 pt-1">
            <input
              type="checkbox"
              id="terms-modal"
              name="acceptTerms"
              checked={formData.acceptTerms}
              onChange={handleInputChange}
              className="mt-1 h-4 w-4 rounded border-slate-300"
              required
            />
            <label htmlFor="terms-modal" className="text-xs text-slate-600">
              Acepto los{" "}
              <Link href="/terminos" className="text-pacific-600 hover:underline" target="_blank">
                Terminos de Servicio
              </Link>{" "}
              y la{" "}
              <Link href="/privacidad" className="text-pacific-600 hover:underline" target="_blank">
                Politica de Privacidad
              </Link>
              . Autorizo el tratamiento de mis datos personales conforme a la Ley 19.628.
            </label>
          </div>

          {/* Disclaimer IA */}
          <div className="p-3 bg-amber-50/80 border border-amber-200 rounded-xl">
            <p className="text-xs text-amber-800">
              <strong>Aviso:</strong> LEIA utiliza inteligencia artificial para orientacion legal general.
              No reemplaza la asesoria de un abogado titulado.
            </p>
          </div>

          <Button
            type="submit"
            variant="pacific"
            size="lg"
            className="w-full mt-2"
            disabled={isLoading}
          >
            {isLoading ? (
              <Loader2 className="h-5 w-5 animate-spin" />
            ) : (
              <>
                {type === "profesional" ? "Crear perfil gratis" : "Crear cuenta"}
                <ArrowRight className="ml-2 h-5 w-5" />
              </>
            )}
          </Button>

          {/* Divider */}
          <div className="relative my-4">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-slate-200"></div>
            </div>
            <div className="relative flex justify-center text-xs">
              <span className="px-2 bg-white/80 text-slate-500">o continua con</span>
            </div>
          </div>

          {/* Social buttons */}
          <div className="grid grid-cols-2 gap-3">
            <Button type="button" variant="outline" size="sm" className="w-full">
              <svg className="h-4 w-4 mr-2" viewBox="0 0 24 24">
                <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
              </svg>
              Google
            </Button>
            <Button type="button" variant="outline" size="sm" className="w-full">
              <svg className="h-4 w-4 mr-2" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2C6.477 2 2 6.477 2 12c0 4.42 2.865 8.164 6.839 9.489.5.092.682-.217.682-.482 0-.237-.008-.866-.013-1.7-2.782.604-3.369-1.341-3.369-1.341-.454-1.155-1.11-1.462-1.11-1.462-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.087 2.91.831.092-.646.35-1.086.636-1.336-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.269 2.75 1.025A9.578 9.578 0 0112 6.836c.85.004 1.705.114 2.504.336 1.909-1.294 2.747-1.025 2.747-1.025.546 1.377.203 2.394.1 2.647.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.578.688.48C19.138 20.161 22 16.418 22 12c0-5.523-4.477-10-10-10z"/>
              </svg>
              GitHub
            </Button>
          </div>
        </form>

        <p className="text-center text-xs text-slate-500 mt-4">
          Ya tienes cuenta?{" "}
          <Link href="/login" className="text-pacific-600 hover:underline">
            Inicia sesion
          </Link>
        </p>

        {type === "usuario" && (
          <p className="text-center text-xs text-slate-500 mt-2">
            Eres profesional legal?{" "}
            <Link href="/unirse" className="text-pacific-600 hover:underline">
              Unete aqui
            </Link>
          </p>
        )}
      </div>
    </div>
  )
}
