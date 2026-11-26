import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  // static 目录下的图片等静态资源会被直接映射到站点根路径，构建时原样复制
  publicDir: 'static',
  // 复用仓库根目录的 .env（只注入 VITE_ 前缀变量）
  envDir: '..',
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      }
    }
  }
})
