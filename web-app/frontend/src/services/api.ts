import axios from 'axios'
import { useAuthStore } from '../stores/authStore'

const api = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // แสดง error message ก่อน redirect
      const message = error.response?.data?.detail || 'Session หมดอายุ กรุณา login ใหม่'
      
      // ใช้ setTimeout เพื่อให้ error message แสดงก่อน
      setTimeout(() => {
        useAuthStore.getState().logout()
        window.location.href = '/login'
      }, 100)
      
      // Return error เพื่อให้ catch block ใน component จัดการได้
      return Promise.reject(new Error(message))
    }
    return Promise.reject(error)
  }
)

export default api