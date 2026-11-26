import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  publicDir: 'static',
  // GitHub Pages 部署在 https://<用户名>.github.io/<仓库名>/ 子路径下，构建时通过 BASE_PATH 传入
  base: process.env.BASE_PATH || '/',
})
