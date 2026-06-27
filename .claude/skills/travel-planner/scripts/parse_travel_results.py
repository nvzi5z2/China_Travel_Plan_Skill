#!/usr/bin/env python3
"""纯数据解析器——各平台旅行搜索 JSON → 统一结构化格式。

不筛选、不排序、不推荐。这些是 LLM 在 Phase 3 的职责。
"""

import json
import sys
from datetime import datetime
from typing import Any


class FlyaiAdapter:
    """飞猪 flyai JSON → 统一格式。"""

    @staticmethod
    def parse_flights(raw: list) -> list:
        """解析航班列表。"""
        flights = []
        for item in raw:
            try:
                flights.append({
                    "flight_no": item.get("flightNo", item.get("flight_no", "")),
                    "airline": item.get("airlineName", item.get("airline", "")),
                    "departure_time": item.get("departureTime", item.get("dep_time", "")),
                    "arrival_time": item.get("arrivalTime", item.get("arr_time", "")),
                    "from_airport": item.get("departureAirport", item.get("from", "")),
                    "from_city": item.get("departureCity", ""),
                    "to_airport": item.get("arrivalAirport", item.get("to", "")),
                    "to_city": item.get("arrivalCity", ""),
                    "cabin": item.get("cabin", "economy"),
                    "price": item.get("price", item.get("ticketPrice", 0)),
                    "direct": item.get("direct", item.get("isDirect", True)),
                    "product_url": item.get("productUrl", item.get("url", "")),
                })
            except (KeyError, TypeError):
                continue
        return flights

    @staticmethod
    def parse_hotels(raw: list) -> list:
        """解析酒店列表。保留所有可用房型，不筛选。"""
        hotels = []
        for item in raw:
            try:
                # 保留所有房型列表，LLM 在 Phase 3 判断哪个合适
                room_types = item.get("roomTypes", item.get("rooms", []))
                if isinstance(room_types, list) and room_types:
                    parsed_rooms = []
                    for r in room_types:
                        if isinstance(r, dict):
                            parsed_rooms.append({
                                "name": r.get("name", r.get("roomName", "")),
                                "bed_type": r.get("bedType", r.get("bed", "")),
                                "price": r.get("price", 0),
                                "capacity": r.get("capacity", r.get("maxGuests", 0)),
                            })
                else:
                    parsed_rooms = []

                hotels.append({
                    "name": item.get("hotelName", item.get("name", "")),
                    "star": item.get("starRating", item.get("star", 0)),
                    "area": item.get("area", item.get("district", "")),
                    "address": item.get("address", ""),
                    "rating": item.get("rating", item.get("userRating", 0)),
                    "room_types": parsed_rooms,
                    "price_from": item.get("priceFrom", item.get("minPrice", 0)),
                    "amenities": item.get("amenities", item.get("facilities", [])),
                    "has_connecting_rooms": item.get("hasConnectingRooms", False),
                    "product_url": item.get("productUrl", item.get("url", "")),
                })
            except (KeyError, TypeError):
                continue
        return hotels

    @staticmethod
    def parse_cars(raw: list) -> list:
        """解析租车列表。保留所有车型，不筛选。"""
        cars = []
        for item in raw:
            try:
                cars.append({
                    "model": item.get("carModel", item.get("model", "")),
                    "type": item.get("carType", item.get("type", "")),
                    "seats": item.get("seats", item.get("maxPassengers", 5)),
                    "transmission": item.get("transmission", "auto"),
                    "price_per_day": item.get("pricePerDay", item.get("dailyPrice", 0)),
                    "company": item.get("company", item.get("vendor", "")),
                    "product_url": item.get("productUrl", item.get("url", "")),
                })
            except (KeyError, TypeError):
                continue
        return cars

    @staticmethod
    def parse_trains(raw: list) -> list:
        """解析火车票列表。"""
        trains = []
        for item in raw:
            try:
                trains.append({
                    "train_no": item.get("trainNo", item.get("train_no", "")),
                    "departure_time": item.get("departureTime", ""),
                    "arrival_time": item.get("arrivalTime", ""),
                    "from_station": item.get("fromStation", ""),
                    "to_station": item.get("toStation", ""),
                    "duration": item.get("duration", ""),
                    "seat_type": item.get("seatType", item.get("seat", "")),
                    "price": item.get("price", 0),
                    "product_url": item.get("productUrl", item.get("url", "")),
                })
            except (KeyError, TypeError):
                continue
        return trains


# 适配器注册表
ADAPTERS = {
    "flyai": FlyaiAdapter(),
    # "ctrip": CtripAdapter(),   # 预留
    # "qunar": QunarAdapter(),   # 预留
}


def parse(raw_data: dict, source: str = "flyai") -> dict:
    """将平台原始 JSON 解析为统一结构化格式。

    Args:
        raw_data: 平台的原始 JSON 响应
        source: 平台标识（flyai / ctrip / qunar）

    Returns:
        {"source": "flyai", "flights": [...], "hotels": [...],
         "cars": [...], "trains": [...], "parsed_at": "ISO8601"}
    """
    adapter = ADAPTERS.get(source)
    if not adapter:
        return {
            "source": source, "flights": [], "hotels": [], "cars": [], "trains": [],
            "error": f"Unknown source: {source}",
            "parsed_at": datetime.now().isoformat(),
        }

    # 兼容不同的 JSON 形状：顶层 array 或 {data: {flights: [...]}}
    data = raw_data
    if isinstance(raw_data, dict):
        data = raw_data.get("data", raw_data.get("result", raw_data))

    flights_raw = data.get("flights", data.get("flightList", [])) if isinstance(data, dict) else []
    hotels_raw = data.get("hotels", data.get("hotelList", [])) if isinstance(data, dict) else []
    cars_raw = data.get("cars", data.get("carList", [])) if isinstance(data, dict) else []
    trains_raw = data.get("trains", data.get("trainList", [])) if isinstance(data, dict) else []

    return {
        "source": source,
        "flights": adapter.parse_flights(flights_raw),
        "hotels": adapter.parse_hotels(hotels_raw),
        "cars": adapter.parse_cars(cars_raw),
        "trains": adapter.parse_trains(trains_raw),
        "parsed_at": datetime.now().isoformat(),
    }


if __name__ == "__main__":
    try:
        raw = json.loads(sys.stdin.read())
        source = raw.get("_source", "flyai") if isinstance(raw, dict) else "flyai"
        result = parse(raw, source=source)
        json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
    except (json.JSONDecodeError, Exception) as e:
        json.dump(
            {"error": str(e), "flights": [], "hotels": [], "cars": [], "trains": []},
            sys.stdout, ensure_ascii=False,
        )
        sys.exit(1)
