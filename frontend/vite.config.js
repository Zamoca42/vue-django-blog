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
      '^/api': 'server.zamoca.space',
      '^/admin': 'server.zamoca.space',
      '^/static': 'server.zamoca.space',
      '^/media': 'server.zamoca.space',
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
