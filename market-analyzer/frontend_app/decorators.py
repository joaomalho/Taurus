from functools import wraps

from django.http import JsonResponse


def login_required_api(view_func):
    """Require authentication for JSON API endpoints (returns 401 instead of redirect)."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper
