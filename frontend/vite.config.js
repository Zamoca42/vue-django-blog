import { resolve } from 'path'

// Plugins
import vue from '@vitejs/plugin-vue'
import vuetify, { transformAssetUrls } from 'vite-plugin-vuetify'

// Utilities
import { defineConfig } from 'vite'
import { fileURLToPath, URL } from 'node:url'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue({ 
      template: { transformAssetUrls }
    }),
    // https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vite-plugin
    vuetify({
      autoImport: true,
    }),
  ],
  define: { 'process.env': {} },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
    extensions: [
      '.js',
      '.json',
      '.jsx',
      '.mjs',
      '.ts',
      '.tsx',
      '.vue',
    ],
  },
  server: {
    port: 3000,
    proxy: {
      // '^/api': 'http://127.0.0.1:8000',
      // '^/admin': 'http://127.0.0.1:8000',
      // '^/static': 'http://127.0.0.1:8000',
      // '^/media': 'http://127.0.0.1:8000',
      '^/api2': 'http://43.201.163.241',
      '^/admin': 'http://43.201.163.241',
      '^/static': 'http://43.201.163.241',
      '^/media': 'http://43.201.163.241',
    }      
  },

  root: resolve(__dirname, 'src', 'pages'),
  publicDir: resolve(__dirname, 'public'),
  
  build: {
    outDir: resolve(__dirname, 'dist'),
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'src', 'pages', 'index.html'),
        // home: resolve(__dirname, 'src', 'pages', 'home.html'),
        list: resolve(__dirname, 'src', 'pages', 'blog', 'post_list.html'),
        detail: resolve(__dirname, 'src', 'pages', 'blog', 'post_detail.html'),
        info: resolve(__dirname, 'src', 'pages', 'Info.html')
      }
    }
  },

})
