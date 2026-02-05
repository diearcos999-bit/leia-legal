import { render, screen, waitFor, act } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { AuthProvider, useAuth } from '@/lib/auth'

// Mock localStorage
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
}
Object.defineProperty(window, 'localStorage', { value: localStorageMock })

// Test component to access auth context
function TestComponent() {
  const auth = useAuth()
  return (
    <div>
      <span data-testid="loading">{auth.isLoading.toString()}</span>
      <span data-testid="authenticated">{auth.isAuthenticated.toString()}</span>
      <span data-testid="user">{auth.user?.email || 'no-user'}</span>
      <button onClick={() => auth.login({ email: 'test@example.com', password: 'TestPass123' })}>
        Login
      </button>
      <button onClick={auth.logout}>Logout</button>
    </div>
  )
}

describe('AuthProvider', () => {
  beforeEach(() => {
    jest.clearAllMocks()
    localStorageMock.getItem.mockReturnValue(null)
  })

  it('renders children', async () => {
    render(
      <AuthProvider>
        <div>Test Content</div>
      </AuthProvider>
    )

    expect(screen.getByText('Test Content')).toBeInTheDocument()
  })

  it('initializes with loading state', () => {
    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    )

    // Initially loading
    expect(screen.getByTestId('loading').textContent).toBe('true')
  })

  it('handles login success', async () => {
    const mockResponse = {
      access_token: 'test-token',
      user: {
        id: 1,
        email: 'test@example.com',
        full_name: 'Test User',
        is_active: true,
        is_verified: false,
        role: 'user',
        created_at: '2024-01-01T00:00:00Z'
      }
    }

    ;(global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse
    })

    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    )

    await waitFor(() => {
      expect(screen.getByTestId('loading').textContent).toBe('false')
    })

    const loginButton = screen.getByText('Login')
    await act(async () => {
      await userEvent.click(loginButton)
    })

    await waitFor(() => {
      expect(screen.getByTestId('authenticated').textContent).toBe('true')
      expect(screen.getByTestId('user').textContent).toBe('test@example.com')
    })
  })

  it('handles login failure', async () => {
    ;(global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
      json: async () => ({ detail: 'Invalid credentials' })
    })

    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    )

    await waitFor(() => {
      expect(screen.getByTestId('loading').textContent).toBe('false')
    })

    const loginButton = screen.getByText('Login')
    await act(async () => {
      await userEvent.click(loginButton)
    })

    await waitFor(() => {
      expect(screen.getByTestId('authenticated').textContent).toBe('false')
    })
  })

  it('handles logout', async () => {
    const mockResponse = {
      access_token: 'test-token',
      user: {
        id: 1,
        email: 'test@example.com',
        full_name: 'Test User',
        is_active: true,
        is_verified: false,
        role: 'user',
        created_at: '2024-01-01T00:00:00Z'
      }
    }

    ;(global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse
    })

    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    )

    await waitFor(() => {
      expect(screen.getByTestId('loading').textContent).toBe('false')
    })

    // Login first
    const loginButton = screen.getByText('Login')
    await act(async () => {
      await userEvent.click(loginButton)
    })

    await waitFor(() => {
      expect(screen.getByTestId('authenticated').textContent).toBe('true')
    })

    // Then logout
    const logoutButton = screen.getByText('Logout')
    await act(async () => {
      await userEvent.click(logoutButton)
    })

    await waitFor(() => {
      expect(screen.getByTestId('authenticated').textContent).toBe('false')
      expect(localStorageMock.removeItem).toHaveBeenCalled()
    })
  })
})

describe('useAuth hook', () => {
  it('throws error when used outside AuthProvider', () => {
    // Suppress console.error for this test
    const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {})

    expect(() => {
      render(<TestComponent />)
    }).toThrow('useAuth must be used within an AuthProvider')

    consoleSpy.mockRestore()
  })
})
