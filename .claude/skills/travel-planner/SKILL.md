---
name: travel-planner
description: Use when the user asks to plan a trip, create a travel itinerary, make a travel guide, or mentions 旅游攻略/旅行计划/出行规划/行程安排. Triggers on requests for multi-day trip planning with food, attractions, and logistics.
---

# Travel Planner

## Overview

Multi-phase travel planning workflow: gather requirements → research → generate MD guide → build mobile HTML → audit for completeness. Acts as a personal travel concierge（专属旅游管家）, not a generic guide generator.

## When to Use

- User asks for trip planning (any duration, any destination)
- User mentions 旅游攻略, 旅行计划, 出行规划, 行程安排
- User wants a mobile-friendly HTML guide for their trip

## Phase 1: Requirements Gathering

Ask questions **one at a time**. Prefer multiple-choice with a "Other" option. Cover:

1. **Departure city + transport mode** (flight/train/drive, specific flight numbers if booked)
2. **Hotel location** (if booked, note to research nearby food later)
3. **Travel style** (food-focused / balanced sightseeing / relaxed pace)
4. **Budget level** (budget / mid-range / premium)
5. **Must-do items** (specific restaurants, attractions, activities user already has in mind)
6. **Travel companions** (solo / couple / family — affects packing list and tone)

**Rule**: First question asks departure city + transport together. Then one question per message. Stop when you have enough to begin research.

**CRITICAL**: Tell user you will search for latest online info (weather, flights, Xiaohongshu/Douyin recommendations, Dianping ratings). Do NOT rely on training data alone.

## Phase 2: Research (Parallel Web Searches)

Launch **4-6 searches simultaneously** across these dimensions:

| Dimension | Search For | Verification |
|-----------|-----------|--------------|
| Weather | `{destination} 天气预报 {dates}` | Cross-check 2+ sources (NMC, AccuWeather) |
| Flights | User's flight numbers + airline + dates | Confirm departure time, terminal, on-time rate, baggage policy |
| Hotel area | `{hotel name} 附近美食 周边 {city}` | Find walking-distance food streets |
| Food trends | `{destination} 美食攻略 小红书 抖音 大众点评 {current year}` | Get trending categories + specific restaurant ratings |
| Attractions | Key attractions + ticket prices + hours + transport | Note Monday closures |
| Events | Local festivals/events during trip dates (e.g., 端午龙舟) | Verify dates match trip |

**Restaurant data standard** — for each recommended restaurant, collect:
- Dianping rating (⭐X.X)
- Average cost per person (¥)
- Distance from hotel (🚶walking/🚕taxi + minutes)
- Must-order dishes (🥢)
- One-line highlight or warning
- **Source URL** where the rating/price was found

### Data Integrity Rules (Anti-Hallucination)

**CRITICAL**: Every factual claim in the final guide must trace back to a search result. If search data is sparse or contradictory, flag it rather than fill gaps with training data.

| Rule | Details |
|------|---------|
| **Source-per-claim** | Every restaurant rating, price, flight detail, ticket price, and event time must have a traceable web search result. |
| **Cross-verify criticals** | Weather: 2+ sources (NMC + AccuWeather). Flights: FlightAware/Airportia + airline site. Events: 2+ local news/media. |
| **Conflict = flag** | If two sources disagree on rating/price/time, present the range and note the conflict. Do NOT pick one silently. |
| **No data = say so** | If a search doesn't return a reliable rating for a restaurant, write "评分暂缺" not a guessed number. If a flight's on-time rate isn't found, don't invent a percentage. |
| **Date-anchor everything** | Weather forecasts, event schedules, and flight data are date-specific. A rating from 2024 is not the same as 2026. Note the year of the source. |
| **Restaurant ratings rule** | Dianping (大众点评) scores are the primary authority for Chinese restaurants. Prefer them over Ctrip/Trip.com scores. If only Ctrip data is available, note the source platform. |

**When search results are insufficient:**
1. Tell the user: "{item}的具体信息在搜索结果中未找到可靠来源，建议出发前自行核实"
2. Do NOT substitute with training data or "common knowledge"
3. If the user insists, provide a suggestion clearly marked with "⚠️ 未经验证"

## Phase 3: MD Guide Generation

Generate a comprehensive Markdown file. Structure:

```markdown
# 🏮 {Trip Title}

> 管家寄语 (one-line personal message)

## 📋 旅行概览 (dates, flights, hotel, weather table)
## ⚠️ 出发前确认 (flight status check, museum booking reminders)
## 🌤️ 天气 (3-day forecast table with dressing advice)
## 🎒 行李清单 (by person: 👫 shared / 🧑 you / 👩 partner)

## 📅 Day 1 · {date} ({weather})
  ### Timeline with: time | activity | detail | 💬管家说 (why) | 🗣️本地人语 (local quotes)

## 📅 Day 2 · {date}
  ...

## 🍽️ 美食推荐 (ranked by social media popularity)
  ### 🔥 Tier 1 (super trending) — 3 restaurants per category
  ### 🔥 Tier 2 (frequently recommended)
  ### 🔥 Tier 3 (specialty snacks)

## 💡 管家贴士 (transport table, pitfall warnings, souvenirs)
## 📞 紧急联系
```

**Tone rules:**
- 私人顾问语气：直接、有用、不说废话
- Each key activity explains WHY, not just WHAT
- Include local sayings and food culture trivia
- Add 💑 romantic moment markers for couples

## Phase 4: HTML Interface Generation

Build a self-contained, mobile-first HTML file. **Reference `template.html`** for the CSS design system and component patterns.

**Design system (parameterized):**
- Color: set `--color-primary` and `--color-accent` to match destination vibe
- Layout: max-width 480px, bottom Tab bar (📅行程/🍽️美食/🎒行李/💡贴士)
- Components: collapsible day cards, timeline with dots, rating badges, checklist items, restaurant mini-cards with map links

**Key interactions:**
- Tab switching (JS, no framework)
- Day card expand/collapse (single JS handler, NO inline onclick)
- Checklist toggle with strikethrough
- Restaurant names link to `https://uri.amap.com/search?keyword={name}`
- Pure CSS/JS, zero external dependencies

## Phase 5: Concierge Audit

After generating both files, systematically check for gaps:

| Check | Details |
|-------|---------|
| 💰 Budget estimate | Total ground cost (excl. flights/hotel) |
| 🌧️ Rain backup | Alternative plans for outdoor activities |
| 📸 Photo spots | Specific locations + angles, especially for female travelers |
| 💧 Hydration | Reminder if temp > 30°C, local drink recommendations |
| 🗣️ Local phrases | 3 survival phrases in local dialect |
| 💑 Romantic moments | Mark sunset/view/lantern spots for couples |
| ⏰ Time buffers | Airport/train departure deadlines + backup transport |

## Anti-Patterns

**Content quality:**
- ❌ Generic "秘制/祖传" restaurant recommendations on tourist main streets
- ❌ Suggesting高铁 when direct taxi is faster and worth the cost for 2+ people
- ❌ Packing list without women's items when partner is female
- ❌ Missing WHY context — every recommendation needs a reason

**Hallucination prevention:**
- ❌ Making up a rating/price when search didn't return one (write "暂缺" instead)
- ❌ Silently picking one value when two sources conflict (present the range)
- ❌ Using training-data "common knowledge" for time-sensitive info (flight times, ticket prices, events)
- ❌ Citing a source without actually having it in search results
- ❌ Presenting 2024 data as current without noting the year

**HTML/UX:**
- ❌ HTML that requires scrolling through entire page (use Tabs)
- ❌ Inline onclick on day headers (causes double-toggle bug with addEventListener)

## Template Reference

See `template.html` for the complete CSS design system and component HTML structure. When generating a new guide, copy the `<style>` block and component patterns, then fill with trip-specific content.
