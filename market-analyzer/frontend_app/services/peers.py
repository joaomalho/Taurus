from backend.datasources.yahoodata import DataHistoryYahoo
from frontend_app.services import stock_data

dh = DataHistoryYahoo()

PEER_METRICS = (
    ("trailingPE", "P/E (TTM)"),
    ("forwardPE", "Forward P/E"),
    ("ROE", "ROE"),
    ("ROA", "ROA"),
    ("OperationalMargin", "Op. Margin"),
    ("CurrentRatio", "Current Ratio"),
    ("GrowthReveneuYoY", "Rev. Growth YoY"),
    ("dividendYield", "Div. Yield"),
)


def _metric_value(fundamentals: dict | None, key: str):
    if not fundamentals or fundamentals.get("error"):
        return None
    kpis = fundamentals.get("kpis", {})
    value = kpis.get(key)
    if value is None or value == "N/A":
        return None
    try:
        if value != value:
            return None
        return round(float(value), 4)
    except (TypeError, ValueError):
        return None


def _peer_row(symbol: str, *, is_subject: bool = False) -> dict:
    bio = stock_data.fetch_bio(symbol)
    fundamentals = dh.get_symbol_fundamental_info(symbol)

    company = symbol
    sector = None
    industry = None
    if isinstance(bio, dict) and "data" in bio:
        payload = bio["data"]
        company = payload.get("LongName") or symbol
        sector = payload.get("Sector")
        industry = payload.get("Industry")

    metrics = {key: _metric_value(fundamentals, key) for key, _ in PEER_METRICS}
    return {
        "symbol": symbol,
        "company": company,
        "sector": sector,
        "industry": industry,
        "is_subject": is_subject,
        "metrics": metrics,
    }


def build_peer_comparison(symbol: str, *, limit: int = 5) -> dict:
    subject = _peer_row(symbol, is_subject=True)
    peer_symbols = dh.get_symbol_peer_symbols(symbol, limit=limit)
    peers = [_peer_row(peer_symbol) for peer_symbol in peer_symbols]

    fundamentals = dh.get_symbol_fundamental_info(symbol) or {}
    sector_pe = _metric_value({"kpis": fundamentals.get("kpis", {})}, "sectorTrailingPE")

    metric_defs = [{"key": key, "label": label} for key, label in PEER_METRICS]
    averages = {}
    for key, _ in PEER_METRICS:
        values = [
            row["metrics"].get(key)
            for row in [subject, *peers]
            if row["metrics"].get(key) is not None
        ]
        averages[key] = round(sum(values) / len(values), 4) if values else None

    return {
        "symbol": symbol,
        "company": subject["company"],
        "sector": subject.get("sector") or "Unknown",
        "industry": subject.get("industry") or "Unknown",
        "sector_trailing_pe": sector_pe,
        "peer_symbols": peer_symbols,
        "subject": subject,
        "peers": peers,
        "averages": averages,
        "metrics": metric_defs,
    }


def build_financial_health_peers(symbol: str, *, limit: int = 3) -> list[dict]:
    comparison = build_peer_comparison(symbol, limit=limit)
    rows = []
    for entry in [comparison["subject"], *comparison["peers"]]:
        fundamentals = dh.get_symbol_fundamental_info(entry["symbol"]) or {}
        kpis = fundamentals.get("kpis", {})
        rows.append({
            "symbol": entry["symbol"],
            "company": entry["company"],
            "sector": entry.get("sector") or comparison["sector"],
            "metrics": {
                "net_debt_ebitda": _metric_value({"kpis": kpis}, "NetDebtEbitda"),
                "interest_coverage": _metric_value({"kpis": kpis}, "InterestCoverageEbit"),
                "current_ratio": _metric_value({"kpis": kpis}, "CurrentRatio"),
                "quick_ratio": _metric_value({"kpis": kpis}, "QuickRatio"),
            },
        })
    return rows
