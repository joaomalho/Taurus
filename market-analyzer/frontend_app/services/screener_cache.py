from django.conf import settings
from django.core.cache import cache

import pandas as pd

from backend.datasources.yahoodata import DataHistoryYahoo

dh = DataHistoryYahoo()

SCREENER_METHODS = {
    "gainers": "get_stocks_gainers",
    "trending": "get_stocks_trending",
    "most_active": "get_stocks_most_active",
}

SCREENER_TTL = getattr(settings, "SCREENER_CACHE_TTL", 900)


def _cache_key(name: str) -> str:
    return f"screener:{name}"


def get_screener(name: str) -> pd.DataFrame | None:
    cached = cache.get(_cache_key(name))
    if cached is None:
        return None
    return pd.DataFrame(cached)


def set_screener(name: str, df: pd.DataFrame | None) -> None:
    if df is None or df.empty:
        return
    cache.set(_cache_key(name), df.to_dict(orient="records"), timeout=SCREENER_TTL)


def refresh_screener(name: str) -> pd.DataFrame | None:
    method_name = SCREENER_METHODS.get(name)
    if not method_name:
        raise ValueError(f"Unknown screener: {name}")

    df = getattr(dh, method_name)()
    set_screener(name, df)
    return df


def get_or_fetch_screener(name: str) -> pd.DataFrame | None:
    df = get_screener(name)
    if df is not None and not df.empty:
        return df
    return refresh_screener(name)


def refresh_all_screeners() -> dict[str, int | str]:
    results: dict[str, int | str] = {}
    for name in SCREENER_METHODS:
        try:
            df = refresh_screener(name)
            results[name] = 0 if df is None else len(df)
        except Exception as exc:
            results[name] = f"error: {exc}"
    return results
