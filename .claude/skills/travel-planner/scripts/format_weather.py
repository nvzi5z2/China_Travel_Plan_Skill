#!/usr/bin/env python3
"""天气数据格式化。

从 stdin 读取天气 JSON（由 web search 结果手工提取），
输出结构化的天气预报表 + 穿衣建议 + 出行提醒。
"""

import json
import sys


def format_weather(weather_data: dict) -> str:
    """将天气数据格式化为 Markdown 表格和穿衣建议。"""
    city = weather_data.get("city", "")
    days = weather_data.get("days", [])
    month = weather_data.get("month", 6)

    lines = []
    lines.append(f"## 🌤️ {city}天气预报")
    lines.append("")
    lines.append("| 日期 | 天气 | 高温 | 低温 | 降水概率 | 风力 |")
    lines.append("|------|------|------|------|----------|------|")

    high_temps = []
    low_temps = []
    has_rain = False

    for d in days:
        date = d.get("date", "-")
        condition = d.get("condition", "-")
        high = d.get("high", "-")
        low = d.get("low", "-")
        rain = d.get("rain_prob", "-")
        wind = d.get("wind", "-")

        lines.append(f"| {date} | {condition} | {high} | {low} | {rain} | {wind} |")

        # 收集温度用于穿衣建议
        try:
            high_temps.append(int(str(high).replace("°", "").replace("C", "")))
            low_temps.append(int(str(low).replace("°", "").replace("C", "")))
        except ValueError:
            pass

        if rain and str(rain) not in ("-", "0%", "0"):
            has_rain = True

    lines.append("")

    # 穿衣建议
    if high_temps and low_temps:
        avg_high = sum(high_temps) / len(high_temps)
        avg_low = sum(low_temps) / len(low_temps)

        lines.append("### 👗 穿衣建议")
        lines.append("")

        if avg_high > 33:
            lines.append("- 🩳 高温天气！短袖、短裤、裙子为主")
            lines.append("- 🧴 防晒：SPF50+ 防晒霜 + 遮阳伞 + 墨镜")
            lines.append("- 💧 每 2 小时补水一次，随身携带电解质饮料")
        elif avg_high > 25:
            lines.append("- 👕 夏装即可：短袖、薄长裤、连衣裙")
            lines.append("- 🧥 备一件薄外套，室内空调/早晚可能偏凉")
        elif avg_high > 15:
            lines.append("- 🧥 春秋装：长袖 + 薄外套，早晚加一件")
            lines.append("- 🧣 如去山区/海边，带防风外套")
        elif avg_high > 5:
            lines.append("- 🧥 冬装：厚外套、毛衣、围巾")
            lines.append("- 🧤 早晚温差大，注意保暖")
        else:
            lines.append("- 🧥🧣 严寒天气！羽绒服、保暖内衣、手套帽子都要带")

        if avg_high - avg_low > 10:
            lines.append(f"- ⚠️ 昼夜温差 {avg_high - avg_low:.0f}°C，早晚注意添衣")
        lines.append("")

    # 雨天提醒
    if has_rain:
        lines.append("### 🌧️ 雨天提醒")
        lines.append("- ☂️ 带折叠伞，不要指望酒店借")
        lines.append("- 👟 备一双防水鞋/拖鞋")
        lines.append("- 📱 手机防水袋（雨天拍照用）")
        lines.append("- 🅱️ 准备室内备选方案（详见每日行程中的雨天备选）")
        lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    try:
        data = json.loads(sys.stdin.read())
        result = format_weather(data)
        print(result)
    except (json.JSONDecodeError, KeyError) as e:
        print(f"天气数据格式错误：{e}", file=sys.stderr)
        sys.exit(1)
