import json
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from frontend_app.decorators import login_required_api
from frontend_app.services.portfolio import (
    build_portfolio_summary,
    parse_avg_cost,
    parse_shares,
)
from users.models import PortfolioPosition
from users.validators import normalize_symbol


@login_required_api
@require_http_methods(["GET"])
def portfolio_list(request):
    return JsonResponse(build_portfolio_summary(request.user))


@login_required_api
@require_http_methods(["POST", "PUT", "PATCH"])
def portfolio_upsert(request):
    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON body."}, status=400)

    try:
        symbol = normalize_symbol(payload.get("symbol", ""))
        shares = parse_shares(payload.get("shares"))
        avg_cost = parse_avg_cost(payload.get("avg_cost"))
    except ValueError as exc:
        return JsonResponse({"error": str(exc)}, status=400)
    except ValidationError as exc:
        message = exc.messages[0] if getattr(exc, "messages", None) else str(exc)
        return JsonResponse({"error": message}, status=400)

    try:
        position = PortfolioPosition.upsert_position(
            request.user,
            symbol,
            shares=shares,
            avg_cost=avg_cost,
        )
    except ValidationError as exc:
        message = exc.messages[0] if getattr(exc, "messages", None) else str(exc)
        return JsonResponse({"error": message}, status=400)

    summary = build_portfolio_summary(request.user)
    return JsonResponse(
        {
            "symbol": position.symbol,
            "shares": float(position.shares),
            "avg_cost": float(position.avg_cost) if position.avg_cost is not None else None,
            "portfolio": summary,
        },
        status=201,
    )


@login_required_api
@require_http_methods(["POST", "DELETE"])
def portfolio_remove(request, symbol: str):
    try:
        symbol = normalize_symbol(symbol)
    except ValidationError as exc:
        message = exc.messages[0] if getattr(exc, "messages", None) else str(exc)
        return JsonResponse({"error": message}, status=400)

    if not PortfolioPosition.remove_position(request.user, symbol):
        return JsonResponse({"error": "Symbol not in portfolio."}, status=404)

    return JsonResponse({"symbol": symbol, "removed": True, "portfolio": build_portfolio_summary(request.user)})
