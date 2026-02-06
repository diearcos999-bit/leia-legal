'use client'

import { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import { useRouter } from 'next/navigation'

// API URL from environment
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// Types
export interface User {
  id: number
  email: string
  full_name: string | null
  is_active: boolean
  is_verified: boolean
  role: string
  created_at: string
}

export type ProfessionalType = 'abogado' | 'procurador' | 'estudio' | null

export interface AuthState {
  user: User | null
  token: string | null
  professionalType: ProfessionalType
  lawyerId: number | null
  isLoading: boolean
  isAuthenticated: boolean
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterData {
  email: string
  password: string
  full_name: string
  rut: string
  phone: string
}

export interface AuthContextType extends AuthState {
  login: (token: string, user: User, professionalType?: ProfessionalType, lawyerId?: number | null) => void
  loginWithCredentials: (credentials: LoginCredentials) => Promise<{ success: boolean; error?: string }>
  register: (data: RegisterData) => Promise<{ success: boolean; error?: string }>
  logout: () => void
  refreshUser: () => Promise<void>
  setProfessionalType: (type: ProfessionalType) => void
}

// Context
const AuthContext = createContext<AuthContextType | undefined>(undefined)

// Token storage keys
const TOKEN_KEY = 'justiciaai_token'
const USER_KEY = 'justiciaai_user'
const PROFESSIONAL_TYPE_KEY = 'justiciaai_professional_type'
const LAWYER_ID_KEY = 'justiciaai_lawyer_id'

// Provider component
export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(null)
  const [professionalType, setProfessionalTypeState] = useState<ProfessionalType>(null)
  const [lawyerId, setLawyerId] = useState<number | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const router = useRouter()

  // Initialize auth state from localStorage
  useEffect(() => {
    const initAuth = async () => {
      try {
        const storedToken = localStorage.getItem(TOKEN_KEY)
        const storedUser = localStorage.getItem(USER_KEY)
        const storedProfessionalType = localStorage.getItem(PROFESSIONAL_TYPE_KEY) as ProfessionalType
        const storedLawyerId = localStorage.getItem(LAWYER_ID_KEY)

        if (storedToken && storedUser) {
          setToken(storedToken)
          setUser(JSON.parse(storedUser))
          setProfessionalTypeState(storedProfessionalType)
          setLawyerId(storedLawyerId ? parseInt(storedLawyerId) : null)

          // Verify token is still valid
          const response = await fetch(`${API_URL}/api/auth/me`, {
            headers: {
              'Authorization': `Bearer ${storedToken}`
            }
          })

          if (response.ok) {
            const userData = await response.json()
            setUser(userData)
            localStorage.setItem(USER_KEY, JSON.stringify(userData))

            // Fetch professional type if user is a lawyer and we don't have it
            if (userData.role === 'lawyer' && !storedProfessionalType) {
              try {
                const profResponse = await fetch(`${API_URL}/api/auth/me/professional`, {
                  headers: { 'Authorization': `Bearer ${storedToken}` }
                })
                if (profResponse.ok) {
                  const profData = await profResponse.json()
                  setProfessionalTypeState(profData.professional_type as ProfessionalType)
                  setLawyerId(profData.id)
                  localStorage.setItem(PROFESSIONAL_TYPE_KEY, profData.professional_type)
                  localStorage.setItem(LAWYER_ID_KEY, profData.id.toString())
                }
              } catch (e) {
                console.error('Error fetching professional type:', e)
              }
            }
          } else {
            // Token expired or invalid
            clearAuth()
          }
        }
      } catch (error) {
        console.error('Error initializing auth:', error)
        clearAuth()
      } finally {
        setIsLoading(false)
      }
    }

    initAuth()
  }, [])

  const clearAuth = () => {
    setToken(null)
    setUser(null)
    setProfessionalTypeState(null)
    setLawyerId(null)
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(USER_KEY)
    localStorage.removeItem(PROFESSIONAL_TYPE_KEY)
    localStorage.removeItem(LAWYER_ID_KEY)
  }

  // Direct login with token and user (used by registration modal)
  const login = (tokenValue: string, userData: User, profType?: ProfessionalType, lawId?: number | null) => {
    setToken(tokenValue)
    setUser(userData)
    localStorage.setItem(TOKEN_KEY, tokenValue)
    localStorage.setItem(USER_KEY, JSON.stringify(userData))

    if (profType) {
      setProfessionalTypeState(profType)
      localStorage.setItem(PROFESSIONAL_TYPE_KEY, profType)
    }
    if (lawId) {
      setLawyerId(lawId)
      localStorage.setItem(LAWYER_ID_KEY, lawId.toString())
    }
  }

  // Login with email and password
  const loginWithCredentials = async (credentials: LoginCredentials): Promise<{ success: boolean; error?: string }> => {
    try {
      const response = await fetch(`${API_URL}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(credentials)
      })

      const data = await response.json()

      if (response.ok) {
        setToken(data.access_token)
        setUser(data.user)
        localStorage.setItem(TOKEN_KEY, data.access_token)
        localStorage.setItem(USER_KEY, JSON.stringify(data.user))

        // Store professional type if present (for lawyers)
        if (data.professional_type) {
          setProfessionalTypeState(data.professional_type as ProfessionalType)
          localStorage.setItem(PROFESSIONAL_TYPE_KEY, data.professional_type)
        }
        if (data.lawyer_id) {
          setLawyerId(data.lawyer_id)
          localStorage.setItem(LAWYER_ID_KEY, data.lawyer_id.toString())
        }

        return { success: true }
      } else {
        return { success: false, error: data.detail || 'Error al iniciar sesión' }
      }
    } catch (error) {
      console.error('Login error:', error)
      return { success: false, error: 'Error de conexión. Verifica que el servidor esté corriendo.' }
    }
  }

  const setProfessionalType = (type: ProfessionalType) => {
    setProfessionalTypeState(type)
    if (type) {
      localStorage.setItem(PROFESSIONAL_TYPE_KEY, type)
    } else {
      localStorage.removeItem(PROFESSIONAL_TYPE_KEY)
    }
  }

  const register = async (data: RegisterData): Promise<{ success: boolean; error?: string }> => {
    try {
      const response = await fetch(`${API_URL}/api/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      })

      const responseData = await response.json()

      if (response.ok) {
        setToken(responseData.access_token)
        setUser(responseData.user)
        localStorage.setItem(TOKEN_KEY, responseData.access_token)
        localStorage.setItem(USER_KEY, JSON.stringify(responseData.user))
        return { success: true }
      } else {
        return { success: false, error: responseData.detail || 'Error al registrarse' }
      }
    } catch (error) {
      console.error('Register error:', error)
      return { success: false, error: 'Error de conexión. Verifica que el servidor esté corriendo.' }
    }
  }

  const logout = () => {
    clearAuth()
    router.push('/')
  }

  const refreshUser = async () => {
    if (!token) return

    try {
      const response = await fetch(`${API_URL}/api/auth/me`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })

      if (response.ok) {
        const userData = await response.json()
        setUser(userData)
        localStorage.setItem(USER_KEY, JSON.stringify(userData))
      } else {
        clearAuth()
      }
    } catch (error) {
      console.error('Error refreshing user:', error)
    }
  }

  const value: AuthContextType = {
    user,
    token,
    professionalType,
    lawyerId,
    isLoading,
    isAuthenticated: !!user && !!token,
    login,
    loginWithCredentials,
    register,
    logout,
    refreshUser,
    setProfessionalType
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

// Hook to use auth context
export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

// HOC for protected routes (client-side)
export function withAuth<P extends object>(Component: React.ComponentType<P>) {
  return function ProtectedRoute(props: P) {
    const { isAuthenticated, isLoading } = useAuth()
    const router = useRouter()

    useEffect(() => {
      if (!isLoading && !isAuthenticated) {
        router.push('/login')
      }
    }, [isLoading, isAuthenticated, router])

    if (isLoading) {
      return (
        <div className="flex items-center justify-center min-h-screen">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        </div>
      )
    }

    if (!isAuthenticated) {
      return null
    }

    return <Component {...props} />
  }
}
