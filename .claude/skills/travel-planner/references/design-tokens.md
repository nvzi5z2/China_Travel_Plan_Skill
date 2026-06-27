# HTML 设计系统参数说明

模板 `assets/template.html` 提供了一套完整的 CSS 设计系统。生成新攻略时，复用 `<style>` 块和组件模式，填入旅行数据。

---

## 主题色参数

通过 CSS 变量实现一键换肤。根据目的地气质设置 4 个核心色：

```css
:root {
  --color-primary: #XX;   /* 主色调，用于标题、徽章、高亮 */
  --color-accent:  #XX;   /* 强调色，用于按钮、价格、评分 */
  --color-bg:      #XX;   /* 页面背景 */
  --color-card:    #XX;   /* 卡片背景 */
}
```

### 配色建议

| 目的地类型 | primary | accent | 感觉 |
|-----------|---------|--------|------|
| 海滨城市（三亚/厦门/青岛） | 深海蓝 #1a5276 | 珊瑚橙 #e67e22 | 清爽放松 |
| 古城古镇（丽江/平遥/潮汕） | 朱砂红 #c0392b | 古铜金 #d4a574 | 底蕴温暖 |
| 都市（北京/上海/成都） | 现代灰 #2c3e50 | 活力蓝 #3498db | 简洁干练 |
| 自然风光（桂林/张家界/九寨沟） | 森林绿 #27ae60 | 阳光黄 #f39c12 | 清新自然 |

更多衍生色自动计算：`--color-primary-light`、`--color-bg-dark`、`--color-text-secondary` 等。

---

## 布局参数

- **最大宽度**：480px（适配主流手机屏幕）
- **底部 Tab 栏高度**：60px
- **卡片圆角**：12px（`--radius-md`）
- **最小触控区域**：44px（符合 iOS/Android 人机交互规范）

---

## 组件库

| 组件 | 用途 |
|------|------|
| `.hero` | 顶部粘性标题，含标题、天气、日期 |
| `.day-card` | 每日行程可折叠卡片，带箭头切换 |
| `.timeline` | 时间线列表，圆点 + 星标 + 特殊标记 |
| `.tl-restaurant` | 时间线内嵌餐厅小卡片 |
| `.restaurant-card` | 独立餐厅卡片，含评分徽章、人均、推荐菜 |
| `.food-grid` | 美食标签页的网格布局 |
| `.checklist` | 交互式行李清单，点击勾选划掉 |
| `.tab-bar` | 底部固定导航栏（📅行程 / 🍽️美食 / 🎒行李 / 💡贴士） |
| `.tab-content` | 标签内容区，靠 `.active` 类切换 |

---

## JS 交互（禁止行内 onclick）

两个全局事件绑定，写在单个 `<script>` 块末尾：

```js
// 底部 Tab 切换
document.querySelectorAll('.tab-btn').forEach(btn =>
  btn.addEventListener('click', () => { /* 切换 .active */ })
);

// 日期卡片展开/收起
document.querySelectorAll('.day-header').forEach(header =>
  header.addEventListener('click', () => { /* 切换 .open */ })
);
```

**禁止**在 HTML 里写 `onclick="..."`，原因：
- `addEventListener` 绑定 + 行内 `onclick` 会导致事件触发两次
- 声明式绑定更易维护和调试

---

## 外部链接规范

| 链接类型 | 格式 |
|---------|------|
| 餐厅地图 | `https://uri.amap.com/search?keyword={省+市+区+店名}` |
| 景点导航 | `https://uri.amap.com/search?keyword={景点全称}` |
| 高德导航（起终点） | `https://uri.amap.com/navigation?from={起点},{}&to={终点},{}` |

> **重要**：高德搜索需要完整地址（省+市+区+店名），模糊关键词可能搜到错误位置。
