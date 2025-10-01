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
    port: 5173,  // Vite dev server port (changed from 3000)
    host: '0.0.0.0',  // Allow access from outside container
    proxy: {
      '/api': {
        target: 'http://backend:8000',  // Use Docker service name
        changeOrigin: true,
      },
    },
  },
})