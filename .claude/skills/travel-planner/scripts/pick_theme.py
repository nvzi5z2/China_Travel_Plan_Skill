#!/usr/bin/env python3
"""根据目的地自动匹配 HTML 主题色。

从 stdin 读取 JSON（城市、类型、季节），输出 CSS 变量块。
"""

import json
import sys

# 目的地→主题色映射。每个城市一套 primary + accent + bg + card
THEME_MAP = {
    # ===== 海滨城市：深海蓝 + 珊瑚橙 =====
    "三亚": {"primary": "#0d4f6b", "accent": "#e67e22", "bg": "#f0f5f8", "card": "#ffffff",
             "label": "海滨度假"},
    "厦门": {"primary": "#1a5276", "accent": "#e8833a", "bg": "#edf2f6", "card": "#ffffff",
             "label": "海岛文艺"},
    "青岛": {"primary": "#1b4f72", "accent": "#d4702c", "bg": "#eef2f5", "card": "#ffffff",
             "label": "红瓦碧海"},
    "大连": {"primary": "#1a5276", "accent": "#e67e22", "bg": "#f0f5f8", "card": "#ffffff",
             "label": "滨海都会"},
    "威海": {"primary": "#1e6b8a", "accent": "#e67e22", "bg": "#f2f7fa", "card": "#ffffff",
             "label": "清新海岸"},
    "北海": {"primary": "#1a6b7a", "accent": "#e8833a", "bg": "#f0f6f7", "card": "#ffffff",
             "label": "南国银滩"},
    "海口": {"primary": "#1a6b7a", "accent": "#e67e22", "bg": "#f0f6f7", "card": "#ffffff",
             "label": "椰风海韵"},

    # ===== 古城古镇：朱砂红 + 古铜金 =====
    "丽江": {"primary": "#b5382e", "accent": "#c4956a", "bg": "#faf6f2", "card": "#fffdfb",
             "label": "纳西古城"},
    "大理": {"primary": "#a8312a", "accent": "#b8946e", "bg": "#f8f4ef", "card": "#fffdfb",
             "label": "苍山洱海"},
    "平遥": {"primary": "#8b3a30", "accent": "#c4a265", "bg": "#f7f3ec", "card": "#fffdfa",
             "label": "晋商古城"},
    "凤凰": {"primary": "#a04030", "accent": "#c9a060", "bg": "#f9f5ef", "card": "#fffdfb",
             "label": "湘西风情"},
    "苏州": {"primary": "#8b3a3a", "accent": "#b8a060", "bg": "#f5f2eb", "card": "#fffefc",
             "label": "江南园林"},
    "杭州": {"primary": "#7a4a3a", "accent": "#b89858", "bg": "#f5f2ec", "card": "#fffefc",
             "label": "人间天堂"},
    "南京": {"primary": "#8b3a30", "accent": "#b8944a", "bg": "#f4f0e8", "card": "#fffefc",
             "label": "六朝古都"},
    "西安": {"primary": "#8b3020", "accent": "#c49530", "bg": "#f5efe4", "card": "#fffdfa",
             "label": "长安故都"},
    "洛阳": {"primary": "#8b3020", "accent": "#c49530", "bg": "#f5efe4", "card": "#fffdfa",
             "label": "神都洛阳"},
    "开封": {"primary": "#8b3a20", "accent": "#c4a040", "bg": "#f5efe4", "card": "#fffdfa",
             "label": "东京梦华"},
    "潮州": {"primary": "#9b3020", "accent": "#d4a050", "bg": "#faf4ee", "card": "#fffdfb",
             "label": "潮汕古城"},
    "汕头": {"primary": "#9b3020", "accent": "#d4a050", "bg": "#faf4ee", "card": "#fffdfb",
             "label": "潮汕风情"},

    # ===== 都市：现代灰 + 活力蓝 =====
    "北京": {"primary": "#1a2a3a", "accent": "#c0392b", "bg": "#f3f4f5", "card": "#ffffff",
             "label": "皇城京韵"},
    "上海": {"primary": "#1c2834", "accent": "#2e86c1", "bg": "#f2f3f5", "card": "#ffffff",
             "label": "摩登上海"},
    "广州": {"primary": "#1a2a30", "accent": "#e63946", "bg": "#f3f5f3", "card": "#ffffff",
             "label": "千年商都"},
    "深圳": {"primary": "#162830", "accent": "#2ecc71", "bg": "#f2f5f3", "card": "#ffffff",
             "label": "创新之都"},
    "成都": {"primary": "#2c2318", "accent": "#e8592c", "bg": "#f6f4f0", "card": "#ffffff",
             "label": "天府之国"},
    "重庆": {"primary": "#2c1a18", "accent": "#e8453c", "bg": "#f4f2f2", "card": "#ffffff",
             "label": "山城雾都"},
    "武汉": {"primary": "#1c2834", "accent": "#e8592c", "bg": "#f3f4f5", "card": "#ffffff",
             "label": "江城武汉"},
    "长沙": {"primary": "#2c1a18", "accent": "#e8453c", "bg": "#f4f2f0", "card": "#ffffff",
             "label": "星城热辣"},
    "天津": {"primary": "#1c2834", "accent": "#2e86c1", "bg": "#f3f4f5", "card": "#ffffff",
             "label": "津门故里"},
    "哈尔滨": {"primary": "#1c2840", "accent": "#c0392b", "bg": "#f2f4f6", "card": "#ffffff",
             "label": "东方莫斯科"},

    # ===== 自然风光：森林绿 + 阳光黄 =====
    "桂林": {"primary": "#1e6e3e", "accent": "#f39c12", "bg": "#f2f7f2", "card": "#ffffff",
             "label": "山水甲天下"},
    "阳朔": {"primary": "#1e6e3e", "accent": "#f39c12", "bg": "#f2f7f2", "card": "#ffffff",
             "label": "阳朔山水"},
    "张家界": {"primary": "#1e5e2e", "accent": "#e8960c", "bg": "#f0f5ee", "card": "#ffffff",
             "label": "奇峰仙境"},
    "九寨沟": {"primary": "#0d5e4a", "accent": "#e8960c", "bg": "#eff6f3", "card": "#ffffff",
             "label": "人间仙境"},
    "黄山": {"primary": "#1a5a3a", "accent": "#e8960c", "bg": "#f0f5f0", "card": "#ffffff",
             "label": "黄山归来"},
    "昆明": {"primary": "#1a6a3a", "accent": "#f39c12", "bg": "#f2f7f2", "card": "#ffffff",
             "label": "春城花都"},
    "贵阳": {"primary": "#1a5a30", "accent": "#f39c12", "bg": "#f0f5f0", "card": "#ffffff",
             "label": "爽爽贵阳"},
    "呼伦贝尔": {"primary": "#2a7a3a", "accent": "#f0b028", "bg": "#f2f7ee", "card": "#ffffff",
             "label": "草原天堂"},
    "拉萨": {"primary": "#1a3a5a", "accent": "#c4952a", "bg": "#f0f2f5", "card": "#ffffff",
             "label": "雪域圣城"},
    "西双版纳": {"primary": "#1a6e3e", "accent": "#e8960c", "bg": "#f2f7f0", "card": "#ffffff",
             "label": "热带风情"},
}

# 城市→类型兜底（THEME_MAP 中未覆盖的城市走这里）
CITY_TYPE_FALLBACK = {
    "珠海": "coastal", "烟台": "coastal", "秦皇岛": "coastal",
    "扬州": "ancient", "绍兴": "ancient", "泉州": "ancient", "喀什": "ancient",
    "沈阳": "urban", "郑州": "urban", "合肥": "urban", "南昌": "urban",
    "南宁": "urban", "福州": "urban", "石家庄": "urban", "太原": "urban",
    "兰州": "urban", "乌鲁木齐": "urban", "呼和浩特": "urban", "银川": "urban",
    "西宁": "urban", "长春": "urban", "济南": "urban",
    "宜昌": "nature", "岳阳": "nature", "庐山": "nature", "峨眉山": "nature",
    "稻城": "nature", "香格里拉": "nature", "林芝": "nature",
}

# 类型→默认主题（完全匹配不到城市时使用）
TYPE_DEFAULTS = {
    "coastal": {"primary": "#1a5276", "accent": "#e67e22", "bg": "#f0f5f8", "card": "#ffffff"},
    "ancient": {"primary": "#8b3a30", "accent": "#c4956a", "bg": "#faf6f2", "card": "#fffdfb"},
    "urban":   {"primary": "#1c2834", "accent": "#2e86c1", "bg": "#f2f3f5", "card": "#ffffff"},
    "nature":  {"primary": "#1e6e3e", "accent": "#f39c12", "bg": "#f2f7f2", "card": "#ffffff"},
}


def pick_theme(city: str, season: str = "spring") -> dict:
    """返回 {primary, accent, bg, card, label, css_block}"""
    # 1. 精确匹配
    if city in THEME_MAP:
        theme = dict(THEME_MAP[city])
        theme["match_type"] = "exact"
        return _build_result(theme, city, season)

    # 2. 模糊匹配（去掉"市"后缀）
    city_clean = city.replace("市", "").replace("县", "")
    if city_clean in THEME_MAP:
        theme = dict(THEME_MAP[city_clean])
        theme["match_type"] = "exact_clean"
        return _build_result(theme, city, season)

    # 3. 类型兜底
    city_type = CITY_TYPE_FALLBACK.get(city, CITY_TYPE_FALLBACK.get(city_clean))
    if city_type and city_type in TYPE_DEFAULTS:
        theme = dict(TYPE_DEFAULTS[city_type])
        theme["match_type"] = "type_fallback"
        theme["label"] = _type_label(city_type)
        return _build_result(theme, city, season)

    # 4. 兜底：通用旅行主题
    theme = {
        "primary": "#2c3e50", "accent": "#3498db",
        "bg": "#f5f6f8", "card": "#ffffff",
        "match_type": "generic_fallback",
        "label": "旅行",
    }
    return _build_result(theme, city, season)


def _type_label(t: str) -> str:
    return {"coastal": "海滨", "ancient": "古城", "urban": "都市", "nature": "自然"}.get(t, "旅行")


def _build_result(theme: dict, city: str, season: str) -> dict:
    """生成完整输出，含 CSS 变量块。"""
    label = theme.get("label", city)

    # 根据季节微调 bg
    bg = theme["bg"]
    if season == "summer":
        bg = _lighten(bg, 0.03)
    elif season == "winter":
        bg = _darken(bg, 0.03)

    css_lines = [
        "        --color-primary: {};".format(theme["primary"]),
        "        --color-accent: {};".format(theme["accent"]),
        "        --color-bg: {};".format(bg),
        "        --color-card: {};".format(theme["card"]),
    ]

    return {
        "city": city,
        "season": season,
        "label": label,
        "match_type": theme.get("match_type", "exact"),
        "primary": theme["primary"],
        "accent": theme["accent"],
        "bg": bg,
        "card": theme["card"],
        "css_block": "\n".join(css_lines),
    }


def _lighten(hex_color: str, amount: float) -> str:
    """简易提亮。"""
    r, g, b = _hex_to_rgb(hex_color)
    r = min(255, int(r + (255 - r) * amount))
    g = min(255, int(g + (255 - g) * amount))
    b = min(255, int(b + (255 - b) * amount))
    return _rgb_to_hex(r, g, b)


def _darken(hex_color: str, amount: float) -> str:
    """简易加深。"""
    r, g, b = _hex_to_rgb(hex_color)
    r = max(0, int(r * (1 - amount)))
    g = max(0, int(g * (1 - amount)))
    b = max(0, int(b * (1 - amount)))
    return _rgb_to_hex(r, g, b)


def _hex_to_rgb(h: str) -> tuple:
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def _rgb_to_hex(r: int, g: int, b: int) -> str:
    return f"#{r:02x}{g:02x}{b:02x}"


if __name__ == "__main__":
    try:
        data = json.loads(sys.stdin.read())
        result = pick_theme(
            city=data.get("city", ""),
            season=data.get("season", "spring"),
        )
        json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
    except (json.JSONDecodeError, KeyError) as e:
        json.dump({"error": str(e)}, sys.stdout, ensure_ascii=False)
        sys.exit(1)
