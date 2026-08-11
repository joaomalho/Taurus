from backend.risk_manager.risk_manager import RiskManagerFundamental
from backend.risk_manager.scoring import score_pillars

DIRECTIONAL_SIGNALS = {"Buy": 1, "Sell": -1, "Flat": 0}

VERDICT_COLORS = {
    "Buy": "#1cf467",
    "Hold": "#6b7280",
    "Sell": "#ff1414",
}

FUNDAMENTAL_WEIGHT = 0.45
TECHNICAL_WEIGHT = 0.55
BUY_THRESHOLD = 0.30
SELL_THRESHOLD = -0.30


def _merge_evaluated_metrics(fundamental_evaluations: dict) -> dict:
    merged = {}
    evaluations = fundamental_evaluations.get("evaluations", fundamental_evaluations)
    if not isinstance(evaluations, dict):
        return merged

    for payload in evaluations.values():
        if isinstance(payload, dict):
            merged.update(payload)
    return merged


def _fundamental_bias(overall_score: float | None) -> tuple[float, list[str]]:
    reasons = []
    if overall_score is None:
        return 0.0, ["Fundamental data unavailable."]

    bias = max(-1.0, min(1.0, (overall_score - 5.0) / 5.0))
    if overall_score >= 7:
        reasons.append(f"Strong fundamentals ({overall_score}/10).")
    elif overall_score >= 5:
        reasons.append(f"Neutral fundamentals ({overall_score}/10).")
    else:
        reasons.append(f"Weak fundamentals ({overall_score}/10).")
    return bias, reasons


def _technical_bias(
    crossover: dict | None,
    adx: dict | None,
    bollinger: dict | None,
    rsi: dict | None,
) -> tuple[float, list[str]]:
    reasons = []
    directional = []

    for label, payload, name in (
        ("EMA crossover", crossover, "crossover"),
        ("Bollinger Bands", bollinger, "bollinger"),
        ("RSI", rsi, "rsi"),
    ):
        if not payload or payload.get("error"):
            continue
        signal = payload.get("signal")
        if signal in DIRECTIONAL_SIGNALS:
            directional.append(DIRECTIONAL_SIGNALS[signal])
            reasons.append(f"{label}: {signal}.")

    if not directional:
        return 0.0, ["Technical signals unavailable or mixed."]

    ta_bias = sum(directional) / len(directional)

    adx_value = None if not adx or adx.get("error") else adx.get("adx_now")
    if adx_value is not None:
        if adx_value < 20:
            ta_bias *= 0.5
            reasons.append(f"ADX {adx_value}: weak trend — lower TA confidence.")
        elif adx_value >= 25:
            reasons.append(f"ADX {adx_value}: trend supports the setup.")
        else:
            reasons.append(f"ADX {adx_value}: moderate trend.")

    return ta_bias, reasons


def _recommendation_bias(fundamental_info: dict | None) -> tuple[float, list[str]]:
    if not fundamental_info or fundamental_info.get("error"):
        return 0.0, []

    sentiment = fundamental_info.get("market_risk_and_sentiment", {})
    if not isinstance(sentiment, dict):
        return 0.0, []

    values = {}
    for key, wrapped in sentiment.items():
        if isinstance(wrapped, dict) and "value" in wrapped:
            values[key] = wrapped["value"]
        else:
            values[key] = wrapped

    mean_rec = values.get("recommendationMean")
    if mean_rec is None:
        return 0.0, []

    try:
        mean_rec = float(mean_rec)
    except (TypeError, ValueError):
        return 0.0, []

    # Yahoo: 1 = Strong Buy … 5 = Strong Sell
    bias = max(-1.0, min(1.0, (3.0 - mean_rec) / 2.0))
    label = {1: "Strong Buy", 2: "Buy", 3: "Hold", 4: "Sell", 5: "Strong Sell"}.get(
        round(mean_rec), f"{mean_rec:.1f}"
    )
    return bias * 0.25, [f"Analyst consensus: {label} ({mean_rec:.2f})."]


def build_decision_verdict(
    *,
    symbol: str,
    fundamental_info: dict | None = None,
    fundamental_evaluations: dict | None = None,
    crossover: dict | None = None,
    adx: dict | None = None,
    bollinger: dict | None = None,
    rsi: dict | None = None,
) -> dict:
    reasons: list[str] = []

    overall_score = None
    pillar_summary = None

    if fundamental_evaluations and not fundamental_evaluations.get("error"):
        merged = _merge_evaluated_metrics(fundamental_evaluations)
        if merged:
            pillar_summary = score_pillars(merged)
            overall_score = pillar_summary.get("overall", {}).get("score")
    elif fundamental_info and not fundamental_info.get("error"):
        rmf = RiskManagerFundamental()
        evaluated = rmf.evaluate_metrics(fundamental_info)
        pillar_summary = score_pillars(evaluated)
        overall_score = pillar_summary.get("overall", {}).get("score")

    fund_bias, fund_reasons = _fundamental_bias(overall_score)
    ta_bias, ta_reasons = _technical_bias(crossover, adx, bollinger, rsi)
    rec_bias, rec_reasons = _recommendation_bias(fundamental_info)

    combined = (
        FUNDAMENTAL_WEIGHT * fund_bias
        + TECHNICAL_WEIGHT * ta_bias
        + rec_bias
    )
    combined = max(-1.0, min(1.0, combined))

    if combined >= BUY_THRESHOLD:
        verdict = "Buy"
    elif combined <= SELL_THRESHOLD:
        verdict = "Sell"
    else:
        verdict = "Hold"

    confidence = round(min(95.0, max(35.0, abs(combined) * 100)), 1)

    if fund_bias > 0.2 and ta_bias > 0.2:
        reasons.append("Fundamentals and technicals align bullish.")
    elif fund_bias < -0.2 and ta_bias < -0.2:
        reasons.append("Fundamentals and technicals align bearish.")
    elif abs(fund_bias - ta_bias) > 0.6:
        reasons.append("Fundamentals and technicals diverge — caution advised.")

    reasons.extend(fund_reasons[:2])
    reasons.extend(ta_reasons[:3])
    reasons.extend(rec_reasons[:1])

    return {
        "symbol": symbol,
        "verdict": verdict,
        "confidence": confidence,
        "score": round(combined, 3),
        "color": VERDICT_COLORS[verdict],
        "components": {
            "fundamental": {
                "bias": round(fund_bias, 3),
                "score_10": overall_score,
                "label": pillar_summary.get("overall", {}).get("label") if pillar_summary else None,
            },
            "technical": {
                "bias": round(ta_bias, 3),
                "signals": {
                    "crossover": (crossover or {}).get("signal"),
                    "adx": (adx or {}).get("signal"),
                    "bollinger": (bollinger or {}).get("signal"),
                    "rsi": (rsi or {}).get("signal"),
                },
            },
            "analyst": {
                "bias": round(rec_bias, 3),
            },
        },
        "reasons": reasons[:6],
        "disclaimer": "Advisory only — not financial advice. Validate before trading.",
    }
