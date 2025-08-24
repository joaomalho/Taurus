# from trading economics
import requests
from datetime import datetime, timedelta, timezone, date


class EcoCalendar():

    def __init__(self) -> None:
        self

    def get_economic_calendar(self, d1: date | datetime | None = None, d2: date | datetime | None = None, timeframe: str | None = "today"):
        """
        Return Economic Calendar from TradingEconomics.
        If `timeframe`, ignore d1/d2 and get interval:
        - "yesterday"
        - "today"
        - "tomorrow"
        - "this week"  -> monday..sunday current week
        - "next week"  -> monday..sunday next week
        """
        url = "https://api.tradingeconomics.com/calendar"
        params = {"format": "json", "c": "guest:guest"}

        def as_date(x):
            if x is None:
                return None
            if isinstance(x, datetime):
                return x.date()
            if isinstance(x, date):
                return x
            raise TypeError(f"Awaits date/datetime, receipt: {type(x)}")

        today = datetime.now(timezone.utc).date()

        if timeframe:
            key = timeframe.strip().lower().replace("_", " ").replace("-", " ")
            if key in {"today"}:
                d1 = d2 = today
            elif key in {"yesterday"}:
                d1 = d2 = today - timedelta(days=1)
            elif key in {"tomorrow"}:
                d1 = d2 = today + timedelta(days=1)
            elif key in {"this week", "current week"}:
                start = today - timedelta(days=today.weekday())
                end = start + timedelta(days=6)
                d1, d2 = start, end
            elif key in {"next week"}:
                start = (today - timedelta(days=today.weekday())) + timedelta(days=7)
                end = start + timedelta(days=6)
                d1, d2 = start, end
            else:
                raise ValueError(f"timeframe inválido: {timeframe}")

        d1 = as_date(d1)
        d2 = as_date(d2)

        if d1 and d2:
            params["d1"] = d1.strftime("%Y-%m-%d")
            params["d2"] = d2.strftime("%Y-%m-%d")

        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        return r.json()
