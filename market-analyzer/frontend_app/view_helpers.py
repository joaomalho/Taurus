from django.http import Http404, JsonResponse

from frontend_app.symbols import normalize_symbol, validate_symbol


def missing_symbol_response():
    return JsonResponse({"error": "Symbol is missing"}, status=400)


def provider_error_response(message: str = "Failed to connect to Yahoo Finance API"):
    return JsonResponse({"error": message}, status=503)


def server_error_response(exc: Exception):
    return JsonResponse({"error": f"Unexpected server error: {str(exc)}"}, status=500)


def error_response(payload: dict, default_status: int = 404):
    if "error" not in payload:
        return None
    return JsonResponse(payload, status=default_status)


def parse_validated_symbol(symbol: str) -> str:
    normalized = normalize_symbol(symbol)
    if not normalized:
        raise ValueError("missing")
    return validate_symbol(normalized)


def symbol_api_view(handler, *, provider_error: str | None = None):
    """Decorator factory for symbol-based JSON API views."""

    def view(request, symbol: str):
        try:
            try:
                validated = parse_validated_symbol(symbol)
            except ValueError:
                return missing_symbol_response()

            result = handler(request, validated)

            if isinstance(result, JsonResponse):
                return result

            if isinstance(result, dict) and "error" in result:
                status = 404
                if result["error"] == "Sem dados":
                    status = 404
                return JsonResponse(result, status=status)

            return JsonResponse(result)

        except Http404:
            raise
        except ConnectionError:
            return provider_error_response(provider_error or "Failed to connect to Yahoo Finance API")
        except Exception as exc:
            return server_error_response(exc)

    return view
