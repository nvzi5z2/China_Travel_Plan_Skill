# China Travel Plan Skill — 旅游规划 Skill

> 最后更新：2026-06-27

## 项目描述

基于 Claude Code 的 AI 旅游规划助手，从需求收集到生成手机端 HTML 攻略，全流程自动化。6 阶段流水线：用户画像 → 需求收集 → 双通道调研（Web + flyai MCP）→ LLM 推理推荐 + MD 攻略 → 移动端 HTML → 管家审计。

核心设计原则：**LLM 做判断，脚本做数据。**

## 项目结构

```
.claude/skills/
├── travel-planner/                  # 主 skill：6 阶段旅行规划
│   ├── SKILL.md                     # 331 行，全中文，Phase 0-5
│   ├── scripts/
│   │   ├── parse_travel_results.py  # flyai JSON → 统一结构化数据
│   │   ├── pick_theme.py            # 目的地自动配色（40+ 城市）
│   │   ├── format_weather.py        # 天气 JSON → MD 表格
│   │   ├── validate_budget.py       # 预算一致性校验
│   │   └── validate_itinerary.py    # 行程时间冲突检测
│   ├── references/
│   │   ├── anti-hallucination.md    # 反幻觉规则 + flyai 数据规则
│   │   ├── cuisine-db.md            # 12 个热门城市美食映射
│   │   ├── amap-api.md              # 高德地图链接生成规范
│   │   └── design-tokens.md         # CSS 设计系统参数
│   ├── assets/
│   │   └── template.html            # 带 4 种卡片组件的 HTML 骨架
│   └── evals/
│       ├── eval_simple_trip.md      # 基础场景
│       ├── eval_family_trip.md      # 2 家庭画像驱动测试
│       └── eval_edge_cases.md       # 边界 + 推荐自洽性审计
│
└── flyai/                           # 飞猪旅行搜索 skill（实时数据源）
    ├── SKILL.md
    └── references/                  # 8 个命令文档
```

## 技术栈

- Python 3（脚本化数据处理）
- Node.js（flyai-cli，飞猪 MCP 接口）
- Claude Code Skills（agentskills.io 标准）
- 飞猪 FlyAI MCP API

## 使用方式

在 Claude Code 中说：「帮我规划一个 XX 旅游」即可自动触发。
