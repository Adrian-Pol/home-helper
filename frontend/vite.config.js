import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from "path"; 

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  base: '/static/react/',
  build: {
    manifest: true,
    outDir: path.resolve(__dirname, '../app/static/react'), // <- absolutna ścieżka
    emptyOutDir: true,
    rollupOptions: {
      input: path.resolve(__dirname, 'index.html'), // <--- WAŻNE
    },
  },
})

