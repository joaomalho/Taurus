"""
Build actionable trade plans from verdict + pattern/technical data.

Priority:
1. Active harmonic pattern (stop not hit, direction aligned)
2. Active candlestick pattern (stop not hit, direction aligned)
3. Bollinger Bands fallback
"""

from __future__ import annotations

from users.models import DEFAULT_PORTFOLIO_VALUE, DEFAULT_RISK_PERCENT as _DEFAULT_RISK_PERCENT

DEFAULT_RISK_PERCENT = float(_DEFAULT_RISK_PERCENT)
EXAMPLE_PORTFOLIO = float(DEFAULT_PORTFOLIO_VALUE)
MIN_RISK_REWARD = 1.0
TP2_MULTIPLIER = 2.0


def _safe_float(value) -> float | None:
    try:
        if value is None:
            return None
        parsed = float(value)
        if parsed != parsed:  # NaN
            return None
        return parsed
    except (TypeError, ValueError):
        return None


def _current_price(bio: dict | None) -> float | None:
    if not bio or bio.get("error"):
        return None
    payload = bio.get("data", bio)
    if not isinstance(payload, dict):
        return None
    return _safe_float(payload.get("CurrentPrice"))


def _pct_change(entry: float, target: float) -> float | None:
    if entry == 0:
        return None
    return round(((target - entry) / entry) * 100, 2)


def _risk_reward(entry: float, stop: float, target: float) -> float | None:
    risk = abs(entry - stop)
    reward = abs(target - entry)
    if risk <= 0:
        return None
    return round(reward / risk, 2)


def _position_hint(
    entry: float,
    stop: float,
    *,
    portfolio_value: float | None = None,
    risk_percent: float | None = None,
) -> dict:
    risk_per_share = abs(entry - stop)
    if risk_per_share <= 0:
        return {}

    portfolio = portfolio_value if portfolio_value is not None else EXAMPLE_PORTFOLIO
    risk_pct = risk_percent if risk_percent is not None else DEFAULT_RISK_PERCENT
    capital_at_risk = portfolio * (risk_pct / 100)
    shares = int(capital_at_risk / risk_per_share)
    return {
        "risk_percent": risk_pct,
        "portfolio_value": round(portfolio, 2),
        "example_portfolio": round(portfolio, 2),
        "capital_at_risk": round(capital_at_risk, 2),
        "shares": max(shares, 0),
    }


def _trailing_stop(side: str, entry: float, stop: float, tp1: float) -> dict:
    risk = abs(entry - stop)
    if risk <= 0:
        return {}

    if side == "Buy":
        description = "At TP1, move stop to breakeven; then trail 1R below the peak."
    else:
        description = "At TP1, move stop to breakeven; then trail 1R above the trough."

    return {
        "activate_at": round(tp1, 4),
        "move_stop_to": round(entry, 4),
        "trail_distance": round(risk, 4),
        "description": description,
    }


def _plan_payload(
    *,
    source: str,
    side: str,
    entry: float,
    stop: float,
    tp1: float,
    tp2: float | None = None,
    tp3: float | None = None,
    label: str | None = None,
    notes: list[str] | None = None,
    portfolio_value: float | None = None,
    risk_percent: float | None = None,
) -> dict:
    targets = {
        "tp1": {
            "price": round(tp1, 4),
            "change_pct": _pct_change(entry, tp1),
            "risk_reward": _risk_reward(entry, stop, tp1),
        }
    }
    if tp2 is not None:
        targets["tp2"] = {
            "price": round(tp2, 4),
            "change_pct": _pct_change(entry, tp2),
            "risk_reward": _risk_reward(entry, stop, tp2),
        }
    if tp3 is not None:
        targets["tp3"] = {
            "price": round(tp3, 4),
            "change_pct": _pct_change(entry, tp3),
            "risk_reward": _risk_reward(entry, stop, tp3),
        }

    rr = targets["tp1"].get("risk_reward")
    return {
        "available": True,
        "source": source,
        "side": side,
        "label": label or source,
        "entry": round(entry, 4),
        "stop_loss": {
            "price": round(stop, 4),
            "change_pct": _pct_change(entry, stop),
        },
        "targets": targets,
        "risk_reward": rr,
        "position_hint": _position_hint(
            entry, stop, portfolio_value=portfolio_value, risk_percent=risk_percent
        ),
        "trailing_stop": _trailing_stop(side, entry, stop, tp1),
        "notes": notes or [],
        "disclaimer": "Advisory only — validate levels before trading.",
    }


def _pick_harmonic(
    harmonic_patterns: dict | None,
    side: str,
    *,
    portfolio_value: float | None = None,
    risk_percent: float | None = None,
) -> dict | None:
    if not harmonic_patterns or harmonic_patterns.get("error"):
        return None

    patterns = harmonic_patterns.get("patterns_detected", [])
    if not isinstance(patterns, list):
        return None

    wanted_direction = 1 if side == "Buy" else -1
    candidates = [
        p for p in patterns
        if p.get("direction") == wanted_direction
        and not p.get("stop_hit")
        and p.get("STOP") is not None
    ]
    if not candidates:
        return None

    # Most recent pattern (highest D_index)
    pattern = max(candidates, key=lambda item: item.get("D_index", -1))
    stop = _safe_float(pattern.get("STOP"))
    tp1 = _safe_float(pattern.get("TP1"))
    if stop is None or tp1 is None:
        return None

    entry = _safe_float(pattern.get("D_price")) or tp1
    return _plan_payload(
        source="harmonic_pattern",
        side=side,
        entry=entry,
        stop=stop,
        tp1=tp1,
        tp2=_safe_float(pattern.get("TP2")),
        tp3=_safe_float(pattern.get("TP3")),
        label=f"{pattern.get('pattern', 'Harmonic')} ({side})",
        notes=[
            f"Harmonic setup from pattern {pattern.get('pattern', 'N/A')}.",
            "Pattern is still open (stop not hit).",
        ],
        portfolio_value=portfolio_value,
        risk_percent=risk_percent,
    )


def _pick_candle(candle_patterns: dict | None, side: str) -> tuple[str, dict, float] | None:
    if not candle_patterns or candle_patterns.get("error"):
        return None

    detected = candle_patterns.get("patterns_detected")
    if not isinstance(detected, dict):
        return None

    wanted_sign = 100 if side == "Buy" else -100
    candidates = []
    for pattern_name, entries in detected.items():
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if entry.get("Result") != "No Hit":
                continue
            signal = entry.get("Signal")
            if signal != wanted_sign:
                continue
            stop = _safe_float(entry.get("Stoploss"))
            if stop is None:
                continue
            candidates.append((pattern_name, entry, stop))

    if not candidates:
        return None

    pattern_name, entry, stop = candidates[-1]
    return pattern_name, entry, stop


def _build_from_candle(
    candle_patterns: dict | None,
    side: str,
    entry: float,
    *,
    portfolio_value: float | None = None,
    risk_percent: float | None = None,
) -> dict | None:
    picked = _pick_candle(candle_patterns, side)
    if not picked:
        return None

    pattern_name, _entry_row, stop = picked
    risk = abs(entry - stop)
    if risk <= 0:
        return None

    if side == "Buy":
        tp1 = entry + (TP2_MULTIPLIER * risk)
        tp2 = entry + (3 * risk)
    else:
        tp1 = entry - (TP2_MULTIPLIER * risk)
        tp2 = entry - (3 * risk)

    return _plan_payload(
        source="candlestick_pattern",
        side=side,
        entry=entry,
        stop=stop,
        tp1=tp1,
        tp2=tp2,
        label=f"{pattern_name.replace('_', ' ').title()} ({side})",
        notes=[
            f"Candlestick pattern: {pattern_name}.",
            "Stop from pattern; TP1/TP2 estimated at 2R and 3R.",
        ],
        portfolio_value=portfolio_value,
        risk_percent=risk_percent,
    )


def _build_from_bollinger(
    bollinger: dict | None,
    side: str,
    entry: float,
    *,
    portfolio_value: float | None = None,
    risk_percent: float | None = None,
) -> dict | None:
    if not bollinger or bollinger.get("error"):
        return None

    lower = _safe_float(bollinger.get("lower_band"))
    upper = _safe_float(bollinger.get("upper_band"))
    if lower is None or upper is None:
        return None

    if side == "Buy":
        stop = lower
        risk = entry - stop
        if risk <= 0:
            return None
        tp1 = entry + (TP2_MULTIPLIER * risk)
        tp2 = upper
    else:
        stop = upper
        risk = stop - entry
        if risk <= 0:
            return None
        tp1 = entry - (TP2_MULTIPLIER * risk)
        tp2 = lower

    rr = _risk_reward(entry, stop, tp1)
    if rr is not None and rr < MIN_RISK_REWARD:
        return None

    return _plan_payload(
        source="bollinger_fallback",
        side=side,
        entry=entry,
        stop=stop,
        tp1=tp1,
        tp2=tp2,
        label=f"Bollinger setup ({side})",
        notes=[
            "No active harmonic/candle setup — using Bollinger bands.",
            f"Bollinger signal: {bollinger.get('signal', 'N/A')}.",
        ],
        portfolio_value=portfolio_value,
        risk_percent=risk_percent,
    )


def build_trade_plan(
    *,
    symbol: str,
    verdict: dict | None,
    bio: dict | None = None,
    harmonic_patterns: dict | None = None,
    candle_patterns: dict | None = None,
    bollinger: dict | None = None,
    portfolio_value: float | None = None,
    risk_percent: float | None = None,
) -> dict:
    if not verdict or verdict.get("error"):
        return {"available": False, "symbol": symbol, "reason": "Verdict unavailable."}

    side = verdict.get("verdict")
    if side not in ("Buy", "Sell"):
        return {
            "available": False,
            "symbol": symbol,
            "reason": "Hold verdict — wait for a clearer Buy/Sell setup.",
        }

    entry = _current_price(bio)
    if entry is None:
        return {
            "available": False,
            "symbol": symbol,
            "reason": "Current price unavailable — cannot build trade plan.",
        }

    harmonic_plan = _pick_harmonic(
        harmonic_patterns, side, portfolio_value=portfolio_value, risk_percent=risk_percent
    )
    if harmonic_plan:
        stop = harmonic_plan["stop_loss"]["price"]
        tp1 = harmonic_plan["targets"]["tp1"]["price"]
        tp2 = harmonic_plan["targets"].get("tp2", {}).get("price")
        tp3 = harmonic_plan["targets"].get("tp3", {}).get("price")
        rebuilt = _plan_payload(
            source=harmonic_plan["source"],
            side=side,
            entry=entry,
            stop=stop,
            tp1=tp1,
            tp2=tp2,
            tp3=tp3,
            label=harmonic_plan["label"],
            notes=harmonic_plan.get("notes"),
            portfolio_value=portfolio_value,
            risk_percent=risk_percent,
        )
        rebuilt["symbol"] = symbol
        return rebuilt

    candle_plan = _build_from_candle(
        candle_patterns, side, entry, portfolio_value=portfolio_value, risk_percent=risk_percent
    )
    if candle_plan:
        candle_plan["symbol"] = symbol
        return candle_plan

    bollinger_plan = _build_from_bollinger(
        bollinger, side, entry, portfolio_value=portfolio_value, risk_percent=risk_percent
    )
    if bollinger_plan:
        bollinger_plan["symbol"] = symbol
        return bollinger_plan

    return {
        "available": False,
        "symbol": symbol,
        "reason": "No aligned pattern or technical fallback available.",
    }
