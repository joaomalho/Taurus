from frontend_app.rate_limit import (
    check_rate_limit,
    is_heavy_api_path,
    is_stock_api_path,
    rate_limit_response,
)


class RateLimitMiddleware:
    """Limit abusive traffic to expensive stock/market JSON endpoints."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "GET" and is_stock_api_path(request.path):
            heavy = is_heavy_api_path(request.path)
            allowed, retry_after = check_rate_limit(request, heavy=heavy)
            if not allowed:
                return rate_limit_response(retry_after)

        return self.get_response(request)
