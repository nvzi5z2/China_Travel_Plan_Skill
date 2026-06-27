# travel-planner — AI 旅游规划 Skill

> 基于 Claude Code 的 AI 旅游规划助手，从需求收集到生成手机端 HTML 攻略，全流程自动化。集成飞猪 flyai 实时搜索机票、酒店、租车。

## 工作流程（6 阶段）

0. **用户画像建立** — 从对话中提取出行组合、饮食限制、体力水平、花钱风格、特殊日子、兴趣标签，作为所有推荐的核心上下文
1. **深度需求收集** — 基于画像针对性收集交通/住宿/租车偏好（不预设房型/车型）
2. **双通道调研** — Web 搜索（天气/美食/景点）+ flyai MCP 实时查询（机票/高铁/酒店/租车）
3. **LLM 推理推荐 + MD 攻略生成** — LLM 结合画像 + flyai 数据逐个评估，每条推荐附「为什么」
4. **HTML 界面生成** — 移动优先单页，含交通卡片（可预订）、酒店卡片（可预订）、租车卡片
5. **管家审计** — 13 项检查（含推荐自洽性、禁忌、体力曲线、地理聚类）

## 文件结构

```
.claude/skills/
├── travel-planner/                       # 旅行规划 skill
│   ├── SKILL.md                          # 6 阶段流程 + LLM 推理指令 + 画像 Schema
│   ├── scripts/                          # 确定性脚本（不做推荐决策）
│   │   ├── parse_travel_results.py       #   flyai JSON → 统一结构化数据
│   │   ├── pick_theme.py                 #   40+ 城市自动配色
│   │   ├── format_weather.py             #   天气格式化
│   │   ├── validate_budget.py            #   预算校验
│   │   └── validate_itinerary.py         #   行程冲突检测
│   ├── references/
│   │   ├── anti-hallucination.md         #   反幻觉 + flyai 数据使用规则
│   │   ├── cuisine-db.md                 #   12 个城市美食映射
│   │   ├── amap-api.md                   #   高德地图链接规范
│   │   └── design-tokens.md              #   CSS 设计系统参数
│   ├── assets/
│   │   └── template.html                 #   含交通/酒店/租车卡片组件
│   └── evals/
│       ├── eval_simple_trip.md           #   基础：单人 2 天北京
│       ├── eval_family_trip.md           #   画像驱动：2 家庭 3 天三亚
│       └── eval_edge_cases.md            #   边界 + LLM 推理质量
│
└── flyai/                                # 飞猪旅行搜索 skill（实时数据源）
    ├── SKILL.md                          #   自动检测旅行意图触发
    └── references/                       #   8 个命令文档
```

## 核心设计原则

- **LLM 做判断，脚本做数据** — 脚本只做数据清洗和结构化，推荐推理由 LLM 完成，每条推荐带基于画像的自然语言解释
- **画像是推理上下文，不是查找表** — 不硬编码「couple → 大床房」，LLM 结合实时选项逐个评估
- **渐进式加载** — SKILL.md 只放核心流程，长文档在 `references/` 中按需加载
- **全中文指令** — 指令语言 = 执行语言 = 输出语言
- **反幻觉优先** — 每条事实必须有搜索来源，flyai 数据标注查询时间
- **可预订** — 交通/酒店卡片集成飞猪商品链接，点击跳转预订

## 使用方式

1. 将 `.claude/skills/` 复制到你的项目目录
2. 确保已安装 flyai CLI：`npm i -g @fly-ai/flyai-cli`
3. 在 Claude Code 中说「帮我规划一个 XX 旅游」
4. 两个 skill 自动加载，协作完成全流程

## 输出物

- **Markdown 攻略**：旅行画像卡片、交通方案（含推荐理由）、住宿推荐（含房型推理）、租车推荐、每日时间线、三级美食推荐、行李清单、管家贴士
- **移动端 HTML**：底部 Tab 导航、交通/酒店/租车预订卡片、可折叠日期卡片、餐厅评分徽章、交互式行李清单

## 依赖

- Python 3（脚本）
- Node.js（flyai-cli）
- `npm i -g @fly-ai/flyai-cli`
