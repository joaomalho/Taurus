import re

from django.core.exceptions import ValidationError

SYMBOL_PATTERN = re.compile(r"^[A-Z0-9.]{1,10}$")


def normalize_symbol(symbol: str) -> str:
    symbol = (symbol or "").strip().upper()
    if not SYMBOL_PATTERN.match(symbol):
        raise ValidationError("Invalid symbol format.")
    return symbol
