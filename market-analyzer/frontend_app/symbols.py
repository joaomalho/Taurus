from django.core.validators import RegexValidator
from django.http import Http404

_SYMBOL_VALIDATOR = RegexValidator(
    regex=r"^[A-Z0-9.]{1,10}$",
    message="Invalid symbol format.",
)


def validate_symbol(symbol: str) -> str:
    """Validate and return an uppercase stock symbol or raise Http404."""
    try:
        _SYMBOL_VALIDATOR(symbol)
        return symbol
    except Exception as exc:
        raise Http404("Invalid stock symbol.") from exc


def normalize_symbol(symbol: str | None) -> str:
    """Strip and uppercase; empty string if input is missing."""
    return (symbol or "").strip().upper()
