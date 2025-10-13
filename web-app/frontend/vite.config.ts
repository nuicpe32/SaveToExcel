import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,  // Vite dev server port
    host: '0.0.0.0',  // Allow access from outside container
    watch: {
      usePolling: true,  // Enable polling for Docker on Windows
    },
    proxy: {
      '/api': {
        target: 'http://backend:8000',  // ใช้ Docker service name ที่ถูกต้อง
        changeOrigin: true,
        rewrite: (path) => path,
      },
    },
  },
})