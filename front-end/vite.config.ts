import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
//
// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    port: process.env.PORT ? parseInt(process.env.PORT) : 3000,
    host: true
  },
  build: {
    outDir: 'dist',
  },
  resolve: {
    alias: {
      '@': '/src',
    },
  },
  build: {
    outDir: 'dist',
    emptyOutDir: true,
  },
});