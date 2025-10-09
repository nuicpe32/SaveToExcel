import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface User {
  id: number
  username: string
  email: string
  full_name: string | null
  position?: string
  phone_number?: string
  line_id?: string
  is_active: boolean
  is_approved: boolean
  rank?: {
    id: number
    rank_short: string
    rank_full: string
    rank_english: string
  }
  role?: {
    id: number
    role_name: string
    role_display: string
    role_description?: string
  }
}

interface AuthState {
  token: string | null
  user: User | null
  setAuth: (token: string, user: User) => void
  logout: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      user: null,
      setAuth: (token, user) => set({ token, user }),
      logout: () => set({ token: null, user: null }),
    }),
    {
      name: 'auth-storage',
    }
  )
)