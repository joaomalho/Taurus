import json

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from frontend_app.decorators import login_required_api
from users.models import WatchlistItem
from users.validators import normalize_symbol


def _serialize_items(items) -> list[dict]:
    return [
        {
            "symbol": item.symbol,
            "created_at": item.created_at.isoformat(),
        }
        for item in items
    ]


@login_required_api
@require_http_methods(["GET"])
def watchlist_list(request):
    items = WatchlistItem.objects.filter(user=request.user)
    return JsonResponse({"symbols": _serialize_items(items)})


@login_required_api
@require_http_methods(["POST"])
def watchlist_add(request):
    try:
        if request.content_type == "application/json":
            payload = json.loads(request.body or "{}")
            symbol = payload.get("symbol", "")
        else:
            symbol = request.POST.get("symbol", "")
        item = WatchlistItem.add_symbol(request.user, symbol)
        return JsonResponse(
            {
                "symbol": item.symbol,
                "created_at": item.created_at.isoformat(),
            },
            status=201,
        )
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON body."}, status=400)
    except ValidationError as exc:
        message = exc.messages[0] if getattr(exc, "messages", None) else str(exc)
        return JsonResponse({"error": message}, status=400)


@login_required_api
@require_http_methods(["POST", "DELETE"])
def watchlist_remove(request, symbol: str):
    try:
        symbol = normalize_symbol(symbol)
    except ValidationError as exc:
        message = exc.messages[0] if getattr(exc, "messages", None) else str(exc)
        return JsonResponse({"error": message}, status=400)

    if not WatchlistItem.remove_symbol(request.user, symbol):
        return JsonResponse({"error": "Symbol not in watchlist."}, status=404)

    return JsonResponse({"symbol": symbol, "removed": True})
