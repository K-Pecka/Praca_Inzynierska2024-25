import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  build: {
    outDir: 'dist' // Ensure this matches Heroku's default static build path
  },
  server: {
    port: process.env.PORT || 3000 // Use Heroku's PORT environment variable
  }
});
