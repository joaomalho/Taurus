from datetime import date, datetime

import requests
from django.core.cache import cache

from backend.datasources.ecocalendar import EcoCalendar

CACHE_TTL_SECONDS = 300
SUPPORTED_TIMEFRAMES = ("today", "yesterday", "tomorrow", "this week", "next week")


def error_payload(message: str) -> dict:
    return {"error": message}


def _cache_key(*, timeframe: str | None, d1: date | None, d2: date | None) -> str:
    if timeframe:
        return f"economic_calendar:timeframe:{timeframe.strip().lower()}"
    return f"economic_calendar:range:{d1}:{d2}"


def _calendar_source() -> str:
    import os

    return "trading_economics" if os.environ.get("TRADING_ECONOMICS_KEY", "").strip() else "forex_factory"


def fetch_economic_calendar(
    *,
    timeframe: str | None = "today",
    d1: date | datetime | None = None,
    d2: date | datetime | None = None,
) -> dict:
    normalized_timeframe = None
    if timeframe:
        normalized_timeframe = timeframe.strip().lower().replace("_", " ").replace("-", " ")
        if normalized_timeframe not in SUPPORTED_TIMEFRAMES:
            return error_payload(
                f"Invalid timeframe. Use one of: {', '.join(SUPPORTED_TIMEFRAMES)}"
            )
        cache_key = _cache_key(timeframe=normalized_timeframe, d1=None, d2=None)
    else:
        if not d1 or not d2:
            return error_payload("Both d1 and d2 are required when timeframe is omitted.")
        cache_key = _cache_key(timeframe=None, d1=d1, d2=d2)

    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    try:
        calendar = EcoCalendar()
        events = calendar.get_economic_calendar(
            d1=d1,
            d2=d2,
            timeframe=normalized_timeframe or timeframe,
        )
    except ValueError as exc:
        return error_payload(str(exc))
    except requests.RequestException:
        return error_payload("Failed to fetch economic calendar.")

    source = _calendar_source()
    payload = {
        "timeframe": normalized_timeframe or "custom",
        "source": source,
        "count": len(events),
        "events": events,
    }
    if source == "forex_factory" and normalized_timeframe == "next week":
        payload["notice"] = (
            "The free feed covers the current week only. "
            "Set TRADING_ECONOMICS_KEY for extended ranges."
        )

    cache.set(cache_key, payload, CACHE_TTL_SECONDS)
    return payload
