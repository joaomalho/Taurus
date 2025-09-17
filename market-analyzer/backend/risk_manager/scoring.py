# === scoring.py ===

from statistics import mean

# 1) bucket -> score (0..1)
BUCKET_SCORE = {
    "verygood": 1.00,
    "good":     0.75,
    "neutral":  0.50,
    "bad":      0.25,
    "verybad":  0.00,
    "nodata":   None,   # ignora em médias
}

# 2) grupos/pilares
PILLARS = {
    "Valuations": [
        "trailingPE",
        "evEbitda",
        "PriceToSale",
        "EquityFCFYield",
        "EnterpriseFCFYield",
    ],
    "Finantial Health": [
        "NetDebtEbitda",
        "InterestCoverageEbit",
        "CurrentRatio",
        "QuickRatio",
    ],
    "Profitability": [
        "OperationalMargin",
        "FcfMargin",
        "ROE",
        "ROA",
    ],
    "Capital Efficiency": [
        "ROIC",
        "EVA",
    ],
    "Growth": [
        "GrowthReveneuYoY",
        "CagrGrowthReveneuYoY",
        "GrowthEPSYoY",
        "CagrGrowthEPSYoY",
    ],
    "Dividends": [
        "divCoverageRate",
        "PayoutRatio",
        "CagrGrowthDividend3y",
        "CagrGrowthDividend5y",
        "ShareHolderYield",
    ],
}

# rótulo da nota (0..10) -> classe textual (opcional)
def label_from_score10(x: float) -> str:
    if x is None:
        return "No Data"
    if x < 2:   return "Very Bad"
    if x < 4:   return "Bad"
    if x < 6:   return "Neutral"
    if x < 8:   return "Good"
    return "Very Good"

COLOR = {
    "Very Bad": "#ff1414",
    "Bad": "#9b3232",
    "Neutral": "#6b7280",
    "Good": "#0f8a3b",
    "Very Good": "#1cf467",
    "No Data": "#9E9E9E",
}

def _to_score(bucket: str):
    if not bucket:
        return None
    return BUCKET_SCORE.get(bucket.lower(), None)

def _avg_ignore_none(values):
    vals = [v for v in values if v is not None]
    return mean(vals) if vals else None

def score_pillars(evaluated_metrics: dict):
    """
    `evaluated_metrics` vem do teu RiskManagerFundamental.evaluate_metrics(...)
    e deve conter chaves tipo "<kpi>_bucket".
    Retorna: dict com notas 0..10 por pilar e nota global.
    """
    pillar_scores_0_1 = {}
    for pillar, kpis in PILLARS.items():
        scores = []
        for k in kpis:
            bucket = evaluated_metrics.get(f"{k}_bucket")
            scores.append(_to_score(bucket))
        pillar_scores_0_1[pillar] = _avg_ignore_none(scores)

    # 0..1 -> 0..10
    pillar_scores_0_10 = {
        p: (round(s*10, 2) if s is not None else None)
        for p, s in pillar_scores_0_1.items()
    }

    # Nota global: média simples dos pilares disponíveis (pesos iguais entre pilares)
    overall0_1 = _avg_ignore_none(list(pillar_scores_0_1.values()))
    overall0_10 = round(overall0_1*10, 2) if overall0_1 is not None else None

    # labels e cores
    labeled = {}
    for p, v in pillar_scores_0_10.items():
        lab = label_from_score10(v)
        labeled[p] = {
            "score": v,
            "label": lab,
            "color": COLOR[lab],
        }

    overall_label = label_from_score10(overall0_10)
    result = {
        "pillars": labeled,
        "overall": {
            "score": overall0_10,
            "label": overall_label,
            "color": COLOR[overall_label],
        }
    }
    return result
