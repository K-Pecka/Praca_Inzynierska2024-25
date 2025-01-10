import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],  // Vue plugin
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'front-end/src') // Update to reflect your folder structure
    }
  },
  build: {
    lib: {
      entry: path.resolve(__dirname, 'front-end/src/main.ts'), // Correct the entry path
      name: 'MyLib',
      fileName: (format) => `my-lib.${format}.js`
    },
    rollupOptions: {
      external: ['vue'],
      output: {
        globals: {
          vue: 'Vue'
        }
      }
    }
  }
});
