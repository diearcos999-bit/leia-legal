'use client'

import { useState, useEffect, useCallback } from 'react'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
const QUESTION_LIMIT = 5
const STORAGE_KEY_USER = 'leia_user'
const STORAGE_KEY_TOKEN = 'leia_token'
const STORAGE_KEY_QUESTIONS = 'leia_question_count'

interface User {
  id: number
  email: string
  full_name: string | null
  rut: string | null
  phone: string | null
  role: string
}

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
  questionCount: number
  canAskQuestion: boolean
  remainingQuestions: number
}

interface LoginData {
  email: string
  password: string
}

interface RegisterData {
  email: string
  password: string
  full_name?: string
  phone?: string
  rut: string
}

export function useAuth() {
  const [authState, setAuthState] = useState<AuthState>({
    user: null,
    token: null,
    isAuthenticated: false,
    isLoading: true,
    questionCount: 0,
    canAskQuestion: true,
    remainingQuestions: QUESTION_LIMIT
  })

  // Cargar estado inicial desde localStorage
  useEffect(() => {
    const storedUser = localStorage.getItem(STORAGE_KEY_USER)
    const storedToken = localStorage.getItem(STORAGE_KEY_TOKEN)
    const storedQuestions = localStorage.getItem(STORAGE_KEY_QUESTIONS)

    const questionCount = storedQuestions ? parseInt(storedQuestions, 10) : 0

    if (storedUser && storedToken) {
      try {
        const user = JSON.parse(storedUser)
        setAuthState({
          user,
          token: storedToken,
          isAuthenticated: true,
          isLoading: false,
          questionCount,
          canAskQuestion: true, // Usuarios registrados sin límite
          remainingQuestions: Infinity
        })
      } catch {
        // Token inválido, limpiar
        localStorage.removeItem(STORAGE_KEY_USER)
        localStorage.removeItem(STORAGE_KEY_TOKEN)
        setAuthState(prev => ({
          ...prev,
          isLoading: false,
          questionCount,
          canAskQuestion: questionCount < QUESTION_LIMIT,
          remainingQuestions: QUESTION_LIMIT - questionCount
        }))
      }
    } else {
      setAuthState(prev => ({
        ...prev,
        isLoading: false,
        questionCount,
        canAskQuestion: questionCount < QUESTION_LIMIT,
        remainingQuestions: QUESTION_LIMIT - questionCount
      }))
    }
  }, [])

  // Incrementar contador de preguntas
  const incrementQuestionCount = useCallback(() => {
    if (authState.isAuthenticated) return // Usuarios autenticados sin límite

    const newCount = authState.questionCount + 1
    localStorage.setItem(STORAGE_KEY_QUESTIONS, newCount.toString())

    setAuthState(prev => ({
      ...prev,
      questionCount: newCount,
      canAskQuestion: newCount < QUESTION_LIMIT,
      remainingQuestions: Math.max(0, QUESTION_LIMIT - newCount)
    }))
  }, [authState.isAuthenticated, authState.questionCount])

  // Login
  const login = useCallback(async (data: LoginData): Promise<{ success: boolean; error?: string }> => {
    try {
      const response = await fetch(`${API_URL}/api/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })

      if (!response.ok) {
        const error = await response.json()
        return { success: false, error: error.detail || 'Error al iniciar sesión' }
      }

      const result = await response.json()

      // Guardar en localStorage
      localStorage.setItem(STORAGE_KEY_USER, JSON.stringify(result.user))
      localStorage.setItem(STORAGE_KEY_TOKEN, result.access_token)

      setAuthState(prev => ({
        ...prev,
        user: result.user,
        token: result.access_token,
        isAuthenticated: true,
        canAskQuestion: true,
        remainingQuestions: Infinity
      }))

      return { success: true }
    } catch (error) {
      return { success: false, error: 'Error de conexión' }
    }
  }, [])

  // Registro
  const register = useCallback(async (data: RegisterData): Promise<{ success: boolean; error?: string }> => {
    try {
      const response = await fetch(`${API_URL}/api/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })

      if (!response.ok) {
        const error = await response.json()
        return { success: false, error: error.detail || 'Error al registrar' }
      }

      const result = await response.json()

      // Guardar en localStorage
      localStorage.setItem(STORAGE_KEY_USER, JSON.stringify(result.user))
      localStorage.setItem(STORAGE_KEY_TOKEN, result.access_token)

      // Resetear contador de preguntas
      localStorage.removeItem(STORAGE_KEY_QUESTIONS)

      setAuthState(prev => ({
        ...prev,
        user: result.user,
        token: result.access_token,
        isAuthenticated: true,
        questionCount: 0,
        canAskQuestion: true,
        remainingQuestions: Infinity
      }))

      return { success: true }
    } catch (error) {
      return { success: false, error: 'Error de conexión' }
    }
  }, [])

  // Logout
  const logout = useCallback(() => {
    localStorage.removeItem(STORAGE_KEY_USER)
    localStorage.removeItem(STORAGE_KEY_TOKEN)

    const questionCount = parseInt(localStorage.getItem(STORAGE_KEY_QUESTIONS) || '0', 10)

    setAuthState({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,
      questionCount,
      canAskQuestion: questionCount < QUESTION_LIMIT,
      remainingQuestions: Math.max(0, QUESTION_LIMIT - questionCount)
    })
  }, [])

  return {
    ...authState,
    login,
    register,
    logout,
    incrementQuestionCount,
    QUESTION_LIMIT
  }
}
