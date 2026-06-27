#!/usr/bin/env python3
"""行程预算合理性校验。

从 stdin 读取 JSON，校验每日预算加总是否与总预算一致，
检查极端低/高预算的合理性，输出校验报告。
"""

import json
import sys

# 中国主要城市人均餐饮参考价（元/人/天）
CITY_MEAL_BENCHMARK = {
    "北京": 120, "上海": 130, "广州": 100, "深圳": 110,
    "成都": 80, "重庆": 70, "杭州": 90, "西安": 70,
    "厦门": 100, "长沙": 80, "三亚": 150, "丽江": 90,
    "大理": 80, "桂林": 70, "南京": 90, "苏州": 90,
    "武汉": 80, "青岛": 100, "哈尔滨": 70, "昆明": 80,
}

# 中国主要城市景点+市内交通日均参考价（元/人/天）
CITY_ACTIVITY_BENCHMARK = {
    "北京": 200, "上海": 180, "广州": 150, "深圳": 160,
    "成都": 120, "重庆": 100, "杭州": 140, "西安": 150,
    "厦门": 140, "长沙": 110, "三亚": 200, "丽江": 150,
    "大理": 120, "桂林": 180, "南京": 130, "苏州": 130,
    "武汉": 110, "青岛": 130, "哈尔滨": 100, "昆明": 120,
}


def validate_budget(itinerary: dict) -> dict:
    """校验预算合理性，返回 {warnings, errors, benchmark}."""
    warnings = []
    errors = []
    benchmark = {}

    city = itinerary.get("city", "")
    days = itinerary.get("days", 0)
    travelers = itinerary.get("travelers", 1)
    budget_total = itinerary.get("budget_total", 0)
    budget_daily = itinerary.get("budget_daily", [])
    budget_level = itinerary.get("budget_level", "mid-range")

    # 1. 每日预算加总校验
    if budget_daily and budget_total:
        daily_sum = sum(budget_daily)
        if abs(daily_sum - budget_total) > budget_total * 0.05:
            errors.append(
                f"每日预算加总({daily_sum}元) 与总预算({budget_total}元) "
                f"偏差 {abs(daily_sum - budget_total)} 元，请核对"
            )

    # 2. 人均预算基准对比
    if city in CITY_MEAL_BENCHMARK and days > 0:
        meal_ref = CITY_MEAL_BENCHMARK[city]
        activity_ref = CITY_ACTIVITY_BENCHMARK[city]
        daily_ref = (meal_ref + activity_ref) * travelers

        benchmark = {
            "city": city,
            "meal_per_person": meal_ref,
            "activity_per_person": activity_ref,
            "daily_reference_total": daily_ref,
            "trip_reference_total": daily_ref * days,
        }

        per_day_actual = budget_total / days if days > 0 else 0

        if budget_level == "budget" and per_day_actual < daily_ref * 0.4:
            warnings.append(
                f"每日人均预算约{per_day_actual/travelers:.0f}元，"
                f"低于{city}基准({(meal_ref+activity_ref)}元/人/天)的40%。"
                f"可能过于紧张，建议留出弹性"
            )
        elif budget_level == "premium" and per_day_actual < daily_ref * 0.8:
            warnings.append(
                f"标注为高端预算但人均{per_day_actual/travelers:.0f}元/天，"
                f"低于{city}中档基准({meal_ref+activity_ref}元/人/天)，"
                f"建议核实预算水平标签"
            )

    return {
        "valid": len(errors) == 0,
        "warnings": warnings,
        "errors": errors,
        "benchmark": benchmark,
    }


if __name__ == "__main__":
    try:
        data = json.loads(sys.stdin.read())
        result = validate_budget(data)
        json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
        sys.exit(0 if result["valid"] else 1)
    except (json.JSONDecodeError, KeyError) as e:
        json.dump({"valid": False, "errors": [str(e)]}, sys.stdout, ensure_ascii=False)
        sys.exit(1)
