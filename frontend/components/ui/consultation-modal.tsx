'use client'

import { useState } from 'react'
import * as Dialog from '@radix-ui/react-dialog'
import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { X, Loader2, CheckCircle2, AlertCircle } from 'lucide-react'
import { Button } from './button'
import { Input } from './input'

// API URL from environment variable with fallback
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// Validation schema
const consultationSchema = z.object({
  name: z.string().min(2, 'El nombre debe tener al menos 2 caracteres'),
  email: z.string().email('Ingresa un email válido'),
  phone: z.string().optional(),
  description: z.string().min(10, 'Describe tu caso con al menos 10 caracteres'),
})

type ConsultationFormData = z.infer<typeof consultationSchema>

interface Lawyer {
  id: number
  name: string
  specialty: string
  experience: string | null
  rating: number
  reviews: number
  location: string | null
  price_min: number | null
  price_max: number | null
  price: string | null
  image: string | null
  cases: number
  success_rate: number | null
  description: string | null
  is_verified: boolean
}

interface ConsultationModalProps {
  isOpen: boolean
  onClose: () => void
  lawyer: Lawyer | null
}

export function ConsultationModal({ isOpen, onClose, lawyer }: ConsultationModalProps) {
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitStatus, setSubmitStatus] = useState<'idle' | 'success' | 'error'>('idle')
  const [errorMessage, setErrorMessage] = useState('')

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<ConsultationFormData>()

  const onSubmit = async (data: ConsultationFormData) => {
    if (!lawyer) return

    setIsSubmitting(true)
    setSubmitStatus('idle')
    setErrorMessage('')

    try {
      const response = await fetch(`${API_URL}/api/consultations`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          lawyer_id: lawyer.id,
          name: data.name,
          email: data.email,
          phone: data.phone || null,
          description: data.description,
        }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Error al enviar la solicitud')
      }

      setSubmitStatus('success')
      reset()

      // Auto close after success
      setTimeout(() => {
        handleClose()
      }, 2000)
    } catch (error) {
      console.error('Error submitting consultation:', error)
      setSubmitStatus('error')
      setErrorMessage(error instanceof Error ? error.message : 'Error al enviar la solicitud')
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleClose = () => {
    reset()
    setSubmitStatus('idle')
    setErrorMessage('')
    onClose()
  }

  // Validate field on blur
  const validateField = (fieldName: keyof ConsultationFormData, value: string) => {
    try {
      const fieldSchema = consultationSchema.shape[fieldName]
      fieldSchema.parse(value)
      return true
    } catch {
      return false
    }
  }

  if (!lawyer) return null

  return (
    <Dialog.Root open={isOpen} onOpenChange={(open) => !open && handleClose()}>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 bg-black/50 z-50 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0" />
        <Dialog.Content className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-lg shadow-lg p-6 w-full max-w-md z-50 max-h-[90vh] overflow-y-auto data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95">
          <div className="flex items-center justify-between mb-4">
            <Dialog.Title className="text-xl font-semibold">
              Solicitar Consulta
            </Dialog.Title>
            <Dialog.Close asChild>
              <button
                className="rounded-full p-1 hover:bg-gray-100 transition-colors"
                aria-label="Cerrar"
              >
                <X className="h-5 w-5" />
              </button>
            </Dialog.Close>
          </div>

          {/* Lawyer Info */}
          <div className="flex items-center gap-3 mb-6 p-3 bg-gray-50 rounded-lg">
            <img
              src={lawyer.image || 'https://via.placeholder.com/48'}
              alt={lawyer.name}
              className="w-12 h-12 rounded-full object-cover"
            />
            <div>
              <p className="font-medium">{lawyer.name}</p>
              <p className="text-sm text-muted-foreground">{lawyer.specialty}</p>
            </div>
          </div>

          {/* Success State */}
          {submitStatus === 'success' && (
            <div className="flex flex-col items-center justify-center py-8">
              <CheckCircle2 className="h-16 w-16 text-green-500 mb-4" />
              <p className="text-lg font-medium text-center mb-2">
                ¡Solicitud enviada!
              </p>
              <p className="text-sm text-muted-foreground text-center">
                {lawyer.name} se pondrá en contacto contigo pronto.
              </p>
            </div>
          )}

          {/* Error State */}
          {submitStatus === 'error' && (
            <div className="flex items-center gap-3 p-3 mb-4 bg-red-50 border border-red-200 rounded-lg">
              <AlertCircle className="h-5 w-5 text-red-500 flex-shrink-0" />
              <p className="text-sm text-red-700">{errorMessage}</p>
            </div>
          )}

          {/* Form */}
          {submitStatus !== 'success' && (
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div>
                <label htmlFor="name" className="block text-sm font-medium mb-1">
                  Nombre completo *
                </label>
                <Input
                  id="name"
                  placeholder="Tu nombre"
                  {...register('name', {
                    required: 'El nombre es requerido',
                    minLength: { value: 2, message: 'El nombre debe tener al menos 2 caracteres' }
                  })}
                  className={errors.name ? 'border-red-500' : ''}
                />
                {errors.name && (
                  <p className="text-xs text-red-500 mt-1">{errors.name.message}</p>
                )}
              </div>

              <div>
                <label htmlFor="email" className="block text-sm font-medium mb-1">
                  Email *
                </label>
                <Input
                  id="email"
                  type="email"
                  placeholder="tu@email.com"
                  {...register('email', {
                    required: 'El email es requerido',
                    pattern: {
                      value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                      message: 'Ingresa un email válido'
                    }
                  })}
                  className={errors.email ? 'border-red-500' : ''}
                />
                {errors.email && (
                  <p className="text-xs text-red-500 mt-1">{errors.email.message}</p>
                )}
              </div>

              <div>
                <label htmlFor="phone" className="block text-sm font-medium mb-1">
                  Teléfono (opcional)
                </label>
                <Input
                  id="phone"
                  type="tel"
                  placeholder="+56 9 1234 5678"
                  {...register('phone')}
                />
              </div>

              <div>
                <label htmlFor="description" className="block text-sm font-medium mb-1">
                  Describe tu caso *
                </label>
                <textarea
                  id="description"
                  placeholder="Explica brevemente tu situación legal..."
                  rows={4}
                  {...register('description', {
                    required: 'La descripción es requerida',
                    minLength: { value: 10, message: 'Describe tu caso con al menos 10 caracteres' }
                  })}
                  className={`w-full px-3 py-2 border rounded-md text-sm resize-none focus:outline-none focus:ring-2 focus:ring-primary ${
                    errors.description ? 'border-red-500' : 'border-gray-300'
                  }`}
                />
                {errors.description && (
                  <p className="text-xs text-red-500 mt-1">{errors.description.message}</p>
                )}
              </div>

              <div className="flex gap-3 pt-2">
                <Button
                  type="button"
                  variant="outline"
                  className="flex-1"
                  onClick={handleClose}
                  disabled={isSubmitting}
                >
                  Cancelar
                </Button>
                <Button
                  type="submit"
                  className="flex-1"
                  disabled={isSubmitting}
                >
                  {isSubmitting ? (
                    <>
                      <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                      Enviando...
                    </>
                  ) : (
                    'Enviar Solicitud'
                  )}
                </Button>
              </div>

              <p className="text-xs text-muted-foreground text-center">
                Al enviar, aceptas nuestros{' '}
                <a href="/terms" className="text-primary hover:underline">
                  términos de servicio
                </a>{' '}
                y{' '}
                <a href="/privacy" className="text-primary hover:underline">
                  política de privacidad
                </a>
                .
              </p>
            </form>
          )}
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  )
}
