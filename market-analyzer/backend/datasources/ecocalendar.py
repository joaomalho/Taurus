import os
from datetime import date, datetime, timedelta, timezone

import requests

FOREX_FACTORY_WEEK_URL = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
TRADING_ECONOMICS_URL = "https://api.tradingeconomics.com/calendar"

IMPACT_MAP = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "holiday": 0,
}


class EcoCalendar:
    def __init__(self) -> None:
        self._session = requests.Session()
        self._session.headers.update({"User-Agent": "Taurus/1.0"})

    def _trading_economics_credentials(self) -> str | None:
        key = os.environ.get("TRADING_ECONOMICS_KEY", "").strip()
        return key or None

    def _resolve_date_range(
        self,
        *,
        d1: date | datetime | None,
        d2: date | datetime | None,
        timeframe: str | None,
    ) -> tuple[date, date, str]:
        today = datetime.now(timezone.utc).date()

        if timeframe:
            key = timeframe.strip().lower().replace("_", " ").replace("-", " ")
            if key in {"today"}:
                start = end = today
            elif key in {"yesterday"}:
                start = end = today - timedelta(days=1)
            elif key in {"tomorrow"}:
                start = end = today + timedelta(days=1)
            elif key in {"this week", "current week"}:
                start = today - timedelta(days=today.weekday())
                end = start + timedelta(days=6)
            elif key in {"next week"}:
                start = (today - timedelta(days=today.weekday())) + timedelta(days=7)
                end = start + timedelta(days=6)
            else:
                raise ValueError(f"Invalid timeframe: {timeframe}")
            return start, end, key

        start = self._as_date(d1) or today
        end = self._as_date(d2) or start
        if end < start:
            raise ValueError("End date must be on or after start date.")
        return start, end, "custom"

    @staticmethod
    def _as_date(value: date | datetime | None) -> date | None:
        if value is None:
            return None
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, date):
            return value
        raise TypeError(f"Expected date/datetime, got {type(value)}")

    def get_economic_calendar(
        self,
        d1: date | datetime | None = None,
        d2: date | datetime | None = None,
        timeframe: str | None = "today",
    ) -> list[dict]:
        start, end, label = self._resolve_date_range(d1=d1, d2=d2, timeframe=timeframe)

        if self._trading_economics_credentials():
            events = self._fetch_trading_economics(start, end)
            source = "trading_economics"
        else:
            events = self._fetch_forex_factory()
            source = "forex_factory"

        filtered = [
            event for event in events
            if start <= event["_event_date"] <= end
        ]
        filtered.sort(key=lambda item: item.get("datetime") or "")

        for event in filtered:
            event.pop("_event_date", None)
            event["source"] = source

        return filtered

    def _fetch_forex_factory(self) -> list[dict]:
        response = self._session.get(FOREX_FACTORY_WEEK_URL, timeout=15)
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, list):
            raise ValueError("Unexpected calendar payload from Forex Factory.")

        events = []
        for raw in payload:
            if not isinstance(raw, dict):
                continue
            event_dt = self._parse_event_datetime(raw.get("date"))
            if event_dt is None:
                continue

            impact_label = str(raw.get("impact") or "Low").strip()
            events.append({
                "datetime": event_dt.isoformat(),
                "_event_date": event_dt.date(),
                "country": raw.get("country") or "",
                "event": raw.get("title") or "",
                "category": raw.get("impact") or "",
                "importance": IMPACT_MAP.get(impact_label.lower(), 1),
                "impact_label": impact_label,
                "actual": self._clean_value(raw.get("actual")),
                "previous": self._clean_value(raw.get("previous")),
                "forecast": self._clean_value(raw.get("forecast")),
                "unit": None,
                "currency": raw.get("country") or "",
            })
        return events

    def _fetch_trading_economics(self, start: date, end: date) -> list[dict]:
        params = {
            "format": "json",
            "c": self._trading_economics_credentials(),
            "d1": start.strftime("%Y-%m-%d"),
            "d2": end.strftime("%Y-%m-%d"),
        }
        response = self._session.get(TRADING_ECONOMICS_URL, params=params, timeout=15)
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, list):
            raise ValueError("Unexpected calendar payload from TradingEconomics.")

        events = []
        for raw in payload:
            if not isinstance(raw, dict):
                continue
            event_dt = self._parse_event_datetime(raw.get("Date"))
            if event_dt is None:
                continue

            importance = raw.get("Importance")
            try:
                importance = int(importance)
            except (TypeError, ValueError):
                importance = 1

            events.append({
                "datetime": event_dt.isoformat(),
                "_event_date": event_dt.date(),
                "country": raw.get("Country") or "",
                "event": raw.get("Event") or "",
                "category": raw.get("Category") or "",
                "importance": importance,
                "impact_label": self._impact_label(importance),
                "actual": self._clean_value(raw.get("Actual")),
                "previous": self._clean_value(raw.get("Previous")),
                "forecast": self._clean_value(raw.get("Forecast") or raw.get("TEForecast")),
                "unit": raw.get("Unit"),
                "currency": raw.get("Currency") or "",
            })
        return events

    @staticmethod
    def _impact_label(importance: int) -> str:
        return {0: "Holiday", 1: "Low", 2: "Medium", 3: "High"}.get(importance, "Low")

    @staticmethod
    def _clean_value(value) -> str | None:
        if value is None:
            return None
        text = str(value).strip()
        return text or None

    @staticmethod
    def _parse_event_datetime(value) -> datetime | None:
        if not value:
            return None
        text = str(value).strip()
        try:
            parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)
            return parsed.astimezone(timezone.utc)
        except ValueError:
            return None
