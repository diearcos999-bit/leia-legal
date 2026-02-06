'use client'

import { useEffect, useState } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { Loader2 } from 'lucide-react'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
const STORAGE_KEY_USER = 'leia_user'
const STORAGE_KEY_TOKEN = 'leia_token'
const STORAGE_KEY_QUESTIONS = 'leia_question_count'

export default function AuthCallbackPage() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const token = searchParams.get('token')
    const userEmail = searchParams.get('user')
    const errorParam = searchParams.get('error')

    if (errorParam) {
      setError('Error en la autenticacion. Intenta nuevamente.')
      setTimeout(() => router.push('/chat'), 3000)
      return
    }

    if (token && userEmail) {
      // Fetch user data from API
      fetch(`${API_URL}/api/auth/me`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
        .then(res => {
          if (!res.ok) throw new Error('Token invalido')
          return res.json()
        })
        .then(userData => {
          // Save to localStorage (same keys as useAuth hook)
          localStorage.setItem(STORAGE_KEY_TOKEN, token)
          localStorage.setItem(STORAGE_KEY_USER, JSON.stringify(userData))
          // Reset question count for registered users
          localStorage.removeItem(STORAGE_KEY_QUESTIONS)

          // Redirect to chat
          router.push('/chat')
        })
        .catch((err) => {
          console.error('OAuth callback error:', err)
          setError('Error al iniciar sesion. Intenta nuevamente.')
          setTimeout(() => router.push('/chat'), 3000)
        })
    } else {
      setError('No se recibieron credenciales. Redirigiendo...')
      setTimeout(() => router.push('/chat'), 2000)
    }
  }, [searchParams, router])

  return (
    <div className="min-h-screen flex items-center justify-center bg-mesh">
      <div className="text-center glass-card p-8 rounded-2xl">
        {error ? (
          <>
            <div className="text-red-500 mb-4">
              <svg className="h-12 w-12 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
            <p className="text-slate-600">{error}</p>
          </>
        ) : (
          <>
            <Loader2 className="h-12 w-12 animate-spin text-pacific-600 mx-auto mb-4" />
            <p className="text-slate-600">Iniciando sesion...</p>
          </>
        )}
      </div>
    </div>
  )
}
