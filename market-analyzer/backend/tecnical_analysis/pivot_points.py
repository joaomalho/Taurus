"""Classic, Fibonacci, and Camarilla pivot point calculations."""

SUPPORTED_METHODS = ("classic", "fibonacci", "camarilla")


def calculate_levels(high: float, low: float, close: float, method: str = "classic") -> dict[str, float]:
    high = float(high)
    low = float(low)
    close = float(close)
    pivot_range = high - low

    if method == "fibonacci":
        pp = (high + low + close) / 3
        return {
            "pp": pp,
            "r1": pp + 0.382 * pivot_range,
            "r2": pp + 0.618 * pivot_range,
            "r3": pp + pivot_range,
            "s1": pp - 0.382 * pivot_range,
            "s2": pp - 0.618 * pivot_range,
            "s3": pp - pivot_range,
        }

    if method == "camarilla":
        return {
            "pp": (high + low + close) / 3,
            "r1": close + pivot_range * 1.1 / 12,
            "r2": close + pivot_range * 1.1 / 6,
            "r3": close + pivot_range * 1.1 / 4,
            "s1": close - pivot_range * 1.1 / 12,
            "s2": close - pivot_range * 1.1 / 6,
            "s3": close - pivot_range * 1.1 / 4,
        }

    # classic (floor pivots)
    pp = (high + low + close) / 3
    return {
        "pp": pp,
        "r1": 2 * pp - low,
        "r2": pp + pivot_range,
        "s1": 2 * pp - high,
        "s2": pp - pivot_range,
        "r3": high + 2 * (pp - low),
        "s3": low - 2 * (high - pp),
    }


def pivot_signal(current_price: float, levels: dict[str, float]) -> str:
    from backend.risk_manager.risk_manager import RiskManagerTechnical

    rmt = RiskManagerTechnical()
    return rmt.signal_decision_pivot(current_price, levels["pp"], levels["r1"], levels["s1"])
