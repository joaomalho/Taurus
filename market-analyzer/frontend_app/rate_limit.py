import hashlib

from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse


HEAVY_PATH_SUFFIXES = (
    "summary",
    "candle_patterns",
    "harmonic_patterns",
    "stock_gainers",
    "stock_trending",
    "stock_most_active",
    "income_download",
    "cashflow_download",
    "balance_sheet_download",
    "income_quarterly_download",
    "cashflow_quarterly_download",
    "balance_sheet_quarterly_download",
)


def get_client_ip(request) -> str:
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "127.0.0.1")


def is_stock_api_path(path: str) -> bool:
    parts = [part for part in path.split("/") if part]
    if len(parts) >= 2 and parts[0] == "economic-calendar" and parts[1] == "events":
        return True
    if len(parts) >= 3 and parts[0] == "stock":
        return True
    if len(parts) >= 2 and parts[0] == "stockbytop" and parts[1] != "":
        return True
    return False


def is_heavy_api_path(path: str) -> bool:
    return any(path.rstrip("/").endswith(suffix) for suffix in HEAVY_PATH_SUFFIXES)


def _increment_counter(key: str, window: int) -> int:
    try:
        return cache.incr(key)
    except ValueError:
        cache.add(key, 1, timeout=window)
        return 1


def check_rate_limit(request, *, heavy: bool = False) -> tuple[bool, int | None]:
    if not getattr(settings, "RATE_LIMIT_ENABLED", True):
        return True, None

    window = getattr(settings, "RATE_LIMIT_WINDOW", 60)
    limit = (
        getattr(settings, "RATE_LIMIT_HEAVY", 20)
        if heavy
        else getattr(settings, "RATE_LIMIT_API", 120)
    )

    ip = get_client_ip(request)
    scope = "heavy" if heavy else "api"
    digest = hashlib.sha1(ip.encode("utf-8")).hexdigest()[:16]
    key = f"ratelimit:{scope}:{digest}"

    count = _increment_counter(key, window)
    if count > limit:
        return False, window

    return True, None


def rate_limit_response(retry_after: int) -> JsonResponse:
    response = JsonResponse(
        {"error": "Rate limit exceeded. Try again later."},
        status=429,
    )
    response["Retry-After"] = str(retry_after)
    return response
