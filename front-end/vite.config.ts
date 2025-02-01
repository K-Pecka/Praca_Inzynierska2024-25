import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vuetify from 'vite-plugin-vuetify'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(),vuetify()],
  resolve: {
    alias: {
      '@': '/src',
    },
  },
  build: {
    outDir: 'dist',
    emptyOutDir: true,
  },
  server: {
    proxy: {
      "/api": {
        target: "https://api.plannder.com/",
        changeOrigin: true,
        secure: false, // Wyłącz, jeśli używasz HTTPS z samopodpisanym certyfikatem
      },
    },
  },
});