# Pet Healing Frontend

前端基于 Vue 3 + Vite。

## 目录结构

```
frontend/
├── index.html          # 入口 HTML
├── package.json
├── vite.config.js      # publicDir 指向 static
├── src/
│   ├── main.js
│   ├── App.vue
│   └── style.css
└── static/
    └── images/         # 图片等静态资源，可通过 /images/xxx.png 直接访问
```

## 说明

- `static/` 下所有文件会被映射到站点根路径，例如 `static/images/pet-waving.png` 对应 `/images/pet-waving.png`。
- Demo 从确认宠物形象开始，经过命名、情绪评估和旅程须知后进入发现页。

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
