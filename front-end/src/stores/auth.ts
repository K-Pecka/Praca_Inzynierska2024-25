// src/store/auth.js

import { ref } from 'vue'
import api from "@/services/api"

const token = ref(localStorage.getItem('token') || null)
const verified = ref(false)

export function useAuth() {
  const login = async (email: string, password: string) => {
    const response = await fetch('https://api.plannder.com/user_auth/login/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    })
    const data = await response.json()
    if (response.ok) {
      token.value = data.access
      console.log(token.value)
      localStorage.setItem('token', data.access)
    } else {
      throw new Error(data.message || 'Login failed')
    }
  }

  const logout = () => {
    token.value = null
    localStorage.removeItem('token')
  }

  const verifyToken = async () => {
    if (!token.value) return false
    try {
      const response = await api.post('/user_auth/token/verify/', {
        token: token.value,
      })
      verified.value = true
      return true
    } catch (error) {
      logout()
      return false
    }
  }

  const isAuthenticated = () => !!token.value && verified.value

  return {
    token,
    login,
    logout,
    verifyToken,
    isAuthenticated,
  }
}
