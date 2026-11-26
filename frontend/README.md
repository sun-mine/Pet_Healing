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
│   ├── PetAvatar.vue
│   └── style.css
└── static/
    └── images/         # 图片等静态资源，可通过 /images/xxx.png 直接访问
```

## 说明

- `static/` 下所有文件会被映射到站点根路径，例如 `static/images/pet-waving.png` 对应 `/images/pet-waving.png`。
- Demo 依次完成形状、颜色、表情和耳朵定制，确认形象后再命名。完成情绪评估和旅程须知后，定制的宠物会出现在主界面，可以通过底部导航进入发现页。
- 「宠物 → 背包」可切换饰品、衣服和场景物品。保存或关闭背包后，装扮会保存在当前浏览器里。
- 「发现 → 失眠 → 助眠冥想」使用 `static/audio/` 下的本地中文引导录音。
- 「我的」可编辑昵称和宠物名称，资料保存在当前浏览器。情绪趋势展示可导出的示例数据。
- 完成首次引导后，重新打开页面会回到宠物主页。可在「我的 → 设置 → 重新定制宠物」修改已保存的形象。

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
