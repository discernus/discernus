import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  css: {
    postcss: './postcss.config.cjs',
  },
  server: {
    port: 3000,
    open: true,
    // Enable debug mode features in development
    host: true, // Allow external connections for debugging
  },
  define: {
    // Enable debug mode in development
    __DEV__: JSON.stringify(process.env.NODE_ENV === 'development'),
    __DEBUG_MODE__: JSON.stringify(process.env.REACT_APP_DEBUG_MODE === 'true'),
  },
  // Improve dev experience with source maps
  build: {
    sourcemap: true,
  },
}) 