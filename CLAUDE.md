# China Travel Plan Skill — AI 旅游规划 Skill

> 最后更新：2026-06-28

## 项目描述

基于 Claude Code 的 AI 旅游规划助手，6 阶段流水线：用户画像 → 需求收集 → 双通道调研（Web + flyai MCP）→ LLM 推理推荐 + MD 攻略 → 移动端 HTML → 14 项管家审计。

集成飞猪 flyai 实时搜索机票、酒店、租车。核心原则：**LLM 做判断，脚本做数据。**

## 项目结构

```
.claude/skills/
├── travel-planner/                       # 旅行规划 skill（v3.0）
│   ├── SKILL.md                          # 6阶段流程 + IO Schema + Gotchas + LLM推理指令
│   ├── scripts/
│   │   ├── parse_travel_results.py       # flyai JSON → 统一结构化数据（纯解析，不做推荐）
│   │   ├── pick_theme.py                 # 40+城市自动配色
│   │   ├── format_weather.py             # 天气JSON→MD表格
│   │   ├── validate_budget.py            # 预算校验
│   │   └── validate_itinerary.py         # 行程时间冲突检测
│   ├── references/
│   │   ├── anti-hallucination.md         # 反幻觉 + flyai数据规则
│   │   ├── cuisine-db.md                 # 12城市美食映射
│   │   ├── amap-api.md                   # 高德地图链接规范
│   │   └── design-tokens.md              # CSS设计系统参数
│   ├── assets/template.html              # 交通/酒店/租车卡片组件
│   └── evals/                            # 3个画像驱动测试
│
└── flyai/                                # 飞猪旅行搜索 skill（实时数据源）
    ├── SKILL.md                          # 自动检测旅行意图
    └── references/                       # 8个命令文档

output/                                    # 生成的攻略示例
├── 青甘大环线10日退休家庭团攻略_V4.md     # 最新版10天攻略（279行）
├── 青甘大环线10日退休家庭团攻略_V4.html   # 最新版HTML（408行）
├── 青甘大环线10日退休家庭团攻略.html      # 10天版HTML
└── 青甘大环线11日退休家庭团攻略.md        # 11天版MD（旧版）
```

## 技术栈

- Python 3（数据处理脚本）
- Node.js（flyai-cli，飞猪MCP接口）
- Claude Code Skills（agentskills.io标准）
- 飞猪FlyAI MCP API
- 大众点评评分（美食数据源）

## 使用方式

1. 确保安装 flyai CLI：`npm i -g @fly-ai/flyai-cli`
2. 在 Claude Code 中说「帮我规划一个XX旅游」自动触发
3. 两个 skill（travel-planner + flyai）协作完成全流程
