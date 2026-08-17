import json
from decimal import Decimal, InvalidOperation

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from frontend_app.decorators import login_required_api
from users.models import DEFAULT_PORTFOLIO_VALUE, DEFAULT_RISK_PERCENT, User


def _serialize_prefs(user: User) -> dict:
    return {
        "portfolio_value": float(user.portfolio_value),
        "risk_percent": float(user.risk_percent),
        "defaults": {
            "portfolio_value": DEFAULT_PORTFOLIO_VALUE,
            "risk_percent": DEFAULT_RISK_PERCENT,
        },
    }


def _parse_decimal(value, *, field: str, min_value: Decimal, max_value: Decimal):
    try:
        parsed = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError(f"{field} must be a number.")

    if parsed < min_value or parsed > max_value:
        raise ValueError(f"{field} must be between {min_value} and {max_value}.")
    return parsed


@login_required_api
@require_http_methods(["GET", "PATCH", "PUT"])
def trading_prefs(request):
    if request.method == "GET":
        return JsonResponse(_serialize_prefs(request.user))

    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON body."}, status=400)

    user = request.user
    updated = False

    if "portfolio_value" in payload:
        try:
            user.portfolio_value = _parse_decimal(
                payload["portfolio_value"],
                field="portfolio_value",
                min_value=Decimal("100"),
                max_value=Decimal("10000000"),
            )
            updated = True
        except ValueError as exc:
            return JsonResponse({"error": str(exc)}, status=400)

    if "risk_percent" in payload:
        try:
            user.risk_percent = _parse_decimal(
                payload["risk_percent"],
                field="risk_percent",
                min_value=Decimal("0.1"),
                max_value=Decimal("10"),
            )
            updated = True
        except ValueError as exc:
            return JsonResponse({"error": str(exc)}, status=400)

    if not updated:
        return JsonResponse({"error": "No valid fields to update."}, status=400)

    user.save(update_fields=["portfolio_value", "risk_percent"])
    return JsonResponse(_serialize_prefs(user))
