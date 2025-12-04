import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Standard Vite config for React. Tailwind is loaded via PostCSS (tailwind.config.js).
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
  }
})
