# 高德地图链接生成指南

攻略中所有餐厅、景点、酒店位置均通过高德地图 URI 链接提供。用户点击后在手机高德 App 中直接打开导航。

---

## 基础格式

```
https://uri.amap.com/search?keyword={关键词}
```

## 关键字规范

### 餐厅
必须包含：**省 + 市 + 区 + 完整店名**

```
✅ https://uri.amap.com/search?keyword=广东省汕头市金平区杏花吴记牛肉火锅
❌ https://uri.amap.com/search?keyword=杏花吴记（可能搜到同名店或错误城市）
```

### 景点
必须包含：**城市 + 景点全称**

```
✅ https://uri.amap.com/search?keyword=北京市故宫博物院
❌ https://uri.amap.com/search?keyword=故宫（缺城市，可能搜到台北故宫）
```

### 导航起终点（可选）
```
https://uri.amap.com/navigation?from={起点经度},{起点纬度}&to={终点经度},{终点纬度}
```

仅在已知精确坐标时使用。多数场景用 keyword 搜索即可。

---

## 常见坑

| 坑 | 说明 |
|---|------|
| 模糊店名 | 「阿强海鲜」这种名字在全国可能有几十家，必须加上区 |
| 商场内餐厅 | 关键字加上商场名：「XX路万象城B1 海底捞」 |
| 新开业餐厅 | 高德可能搜不到，用百度地图 `https://api.map.baidu.com/geocoder?address={地址}` 作备选 |
| 连锁店 | 必须加具体分店名和区域，否则随机跳到某家分店 |

---

## 生成检查清单

- [ ] 是否包含省+市+区？
- [ ] 店名是否完整（包含分店名）？
- [ ] 是否用 `encodeURIComponent` 编码了中文字符（JS 动态生成链接时）？
- [ ] 是否是 `https://` 而非 `http://`？
