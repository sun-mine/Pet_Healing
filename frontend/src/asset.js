// 拼接静态资源地址，兼容本地开发和 GitHub Pages 子路径部署
export function asset(path) {
  return `${import.meta.env.BASE_URL}${path.replace(/^\/+/, '')}`
}
