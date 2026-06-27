#!/usr/bin/env python3
"""行程时间冲突检测。

从 stdin 读取每日时间线 JSON，检测：
- 相邻活动之间交通时间是否合理
- 同一时段是否有重叠安排
- 用餐时间是否被挤占
"""

import json
import sys
from datetime import datetime, timedelta


# 城市景点间参考交通时间（分钟）
def estimate_transit(city: str, from_place: str, to_place: str) -> int:
    """简易交通时间估算。实际应由在线搜索获取，此处作兜底。"""
    # 默认市内交通 30 分钟
    return 30


def parse_time(time_str: str) -> datetime:
    """解析 '09:30' 或 '14:00' 格式的时间字符串。"""
    return datetime.strptime(time_str.strip(), "%H:%M")


def validate_itinerary(timeline: dict) -> dict:
    """校验单日行程，返回冲突和警告列表。"""
    warnings = []
    errors = []
    activities = timeline.get("activities", [])

    if len(activities) < 2:
        return {"valid": True, "warnings": [], "errors": []}

    for i in range(len(activities) - 1):
        curr = activities[i]
        next_ = activities[i + 1]

        curr_end_str = curr.get("end_time", curr.get("time", ""))
        next_start_str = next_.get("time", "")

        if not curr_end_str or not next_start_str:
            continue

        try:
            curr_end = parse_time(curr_end_str)
            next_start = parse_time(next_start_str)
        except ValueError:
            continue

        gap_min = (next_start - curr_end).total_seconds() / 60

        # 冲突检测
        if gap_min < 0:
            errors.append(
                f"时间重叠：{curr.get('name')}(结束{curr_end_str}) "
                f"与 {next_.get('name')}(开始{next_start_str}) "
                f"重叠 {abs(gap_min):.0f} 分钟"
            )
        elif gap_min < 10:
            warnings.append(
                f"衔接过紧：{curr.get('name')} → {next_.get('name')} "
                f"仅间隔 {gap_min:.0f} 分钟，实际可能来不及"
            )

        # 用餐时间保护
        for act in activities:
            if act.get("type") == "meal" and act.get("time"):
                try:
                    meal_time = parse_time(act["time"])
                    if meal_time.hour < 11 or (meal_time.hour == 11 and meal_time.minute < 0):
                        warnings.append(f"用餐偏早：{act.get('name')} 安排在 {act['time']}")
                    if meal_time.hour > 13 and meal_time.hour < 17:
                        warnings.append(f"午餐偏晚：{act.get('name')} 安排在 {act['time']}")
                except ValueError:
                    pass

    # 检查是否遗漏用餐时段
    has_lunch = any(
        a.get("type") == "meal" and "午" in a.get("name", "")
        for a in activities
    )
    has_dinner = any(
        a.get("type") == "meal" and ("晚" in a.get("name", "") or "夜" in a.get("name", ""))
        for a in activities
    )
    if not has_lunch:
        warnings.append("当天未安排午餐时段")
    if not has_dinner:
        warnings.append("当天未安排晚餐时段")

    return {
        "valid": len(errors) == 0,
        "warnings": warnings,
        "errors": errors,
    }


if __name__ == "__main__":
    try:
        data = json.loads(sys.stdin.read())
        result = validate_itinerary(data)
        json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
        sys.exit(0 if result["valid"] else 1)
    except (json.JSONDecodeError, KeyError) as e:
        json.dump({"valid": False, "errors": [str(e)]}, sys.stdout, ensure_ascii=False)
        sys.exit(1)
