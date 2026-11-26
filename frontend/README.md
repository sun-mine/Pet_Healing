# Pet Healing Frontend

前端基于 Vue 3 + Vite。

## 目录结构

```
frontend/
├── index.html          # 入口 HTML
├── package.json
├── vite.config.js      # publicDir 指向 static，envDir 指向仓库根目录
├── src/
│   ├── main.js
│   ├── App.vue
│   └── style.css
└── static/
    └── images/         # 图片等静态资源，可通过 /images/xxx.png 直接访问
```

## 说明

- `static/` 下所有文件会被映射到站点根路径，例如 `static/images/hero.png` 对应 `/images/hero.png`。
- 环境变量读取仓库根目录的 `.env`，只有 `VITE_` 开头的变量会注入前端。
- 开发环境下 `/api` 请求会被代理到后端 `http://127.0.0.1:8000`。

## 运行

```bash
cd frontend
npm install
npm run dev
```

构建：

```bash
npm run build
```
