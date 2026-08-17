from datetime import datetime, timezone

import numpy as np
import pandas as pd

from backend.datasources.yahoodata import DataHistoryYahoo
from backend.risk_manager.risk_manager import RiskManagerFundamental
from frontend_app.services.peers import build_financial_health_peers

dh = DataHistoryYahoo()


def error_payload(message: str) -> dict:
    return {"error": message}


def fetch_bio(symbol: str) -> dict:
    bio_info = dh.get_symbol_bio_info(symbol)
    if not bio_info:
        return error_payload("No data found")
    bio_info = {k: (None if v == "N/A" else v) for k, v in bio_info.items()}
    return {"data": bio_info}


def fetch_news(symbol: str) -> dict:
    news = dh.get_yahoo_symbol_news(symbol)
    if not news:
        return error_payload("No data found")

    from frontend_app.services.news_sentiment import analyze_news

    analyzed = analyze_news(news)
    return {
        "data": news,
        "items": analyzed["items"],
        "sentiment": analyzed["aggregate"],
    }


def fetch_data_history(symbol: str, period: str = "1y", interval: str = "1d") -> dict:
    df = dh.get_data_history(symbol=symbol, period=period, interval=interval)
    if df is None or df.empty:
        return error_payload("No data found")
    return {"data": df.to_dict(orient="records"), "_df": df}


def get_history_dataframe(
    symbol: str,
    period: str = "1mo",
    interval: str = "1d",
) -> pd.DataFrame | None:
    df = dh.get_data_history(symbol=symbol, period=period, interval=interval)
    if df is None or df.empty:
        return None
    return df


def fetch_inside_transactions(symbol: str) -> dict:
    df = dh.get_symbol_inside_transactions(symbol)
    if df is None or df.empty:
        return error_payload("No data found")

    df = df.copy()
    df["StartDate"] = (
        pd.to_datetime(df["StartDate"], utc=True)
        .dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    )
    df["Shares"] = pd.to_numeric(df["Shares"], errors="coerce")
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
    df = df.replace({np.nan: None})
    return {"data": df.to_dict(orient="records")}


def fetch_fundamental_info(symbol: str) -> dict:
    raw = dh.get_symbol_fundamental_info(symbol)
    if not raw:
        return error_payload("No data found")

    cleaned_data = {}
    for category, data in raw.items():
        cleaned_data[category] = {
            key: {"value": None if value is np.nan else value}
            for key, value in data.items()
        }
    return cleaned_data


def fetch_fundamental_evaluations(symbol: str) -> dict:
    raw = dh.get_symbol_fundamental_info(symbol)
    if not raw:
        return error_payload("No data found")

    rmf = RiskManagerFundamental()
    evaluations_data = {}
    for category, data in raw.items():
        evaluation_result = rmf.evaluate_metrics({category: data})
        evaluations_data[category] = evaluation_result if isinstance(evaluation_result, dict) else {}

    return {"evaluations": evaluations_data}


def fetch_fundamentals(symbol: str) -> dict:
    raw = dh.get_symbol_fundamental_info(symbol)
    if not raw:
        err = error_payload("No data found")
        return {"fundamental_info": err, "fundamental_evaluations": err}

    cleaned_data = {}
    for category, data in raw.items():
        cleaned_data[category] = {
            key: {"value": None if value is np.nan else value}
            for key, value in data.items()
        }

    rmf = RiskManagerFundamental()
    evaluations_data = {}
    for category, data in raw.items():
        evaluation_result = rmf.evaluate_metrics({category: data})
        evaluations_data[category] = evaluation_result if isinstance(evaluation_result, dict) else {}

    return {
        "fundamental_info": cleaned_data,
        "fundamental_evaluations": {"evaluations": evaluations_data},
    }


def fetch_institutional_holders(symbol: str) -> dict:
    df = dh.get_symbol_institutional_holders(symbol)
    if df is None or df.empty:
        return error_payload("No data found")
    df = df.replace({np.nan: None})
    return {"data": df.to_dict(orient="records")}


def fetch_recommendations(symbol: str) -> dict:
    df = dh.get_symbol_recommendations(symbol)
    if df is None or df.empty:
        return error_payload("No data found")
    df = df.replace({np.nan: None})
    return {"data": df.to_dict(orient="records")}


def fetch_earnings_dates(symbol: str) -> dict:
    df = dh.get_yahoo_symbol_earnings_dates(symbol)

    if df is None or not isinstance(df, pd.DataFrame) or df.empty:
        return {"data": []}

    df = df.copy()
    df.columns = [str(col).strip() for col in df.columns]
    df = df.sort_index()

    def _column(*names):
        for name in names:
            if name in df.columns:
                return name
        return None

    event_col = _column("Event Type", "EventType", "event_type")
    if event_col:
        df = df[df[event_col].astype(str).str.lower() == "earnings"]

    if df.empty:
        return {"data": []}

    eps_est_col = _column("EPS Estimate", "Eps Estimate", "eps_estimate")
    reported_col = _column("Reported EPS", "Reported Eps", "reported_eps")
    surprise_col = _column("Surprise(%)", "Surprise (%)", "surprise_pct")

    rows = []
    for idx, row in df.iterrows():
        dt = pd.to_datetime(idx, utc=True, errors="coerce")
        if pd.isna(dt):
            continue

        eps_estimate = row[eps_est_col] if eps_est_col else None
        reported_eps = row[reported_col] if reported_col else None
        surprise_pct = row[surprise_col] if surprise_col else None
        event_type = row[event_col] if event_col else "Earnings"

        rows.append({
            "datetime": dt.isoformat(),
            "eps_estimate": float(eps_estimate) if eps_est_col and pd.notna(eps_estimate) else None,
            "reported_eps": float(reported_eps) if reported_col and pd.notna(reported_eps) else None,
            "surprise_pct": float(surprise_pct) if surprise_col and pd.notna(surprise_pct) else None,
            "event_type": str(event_type) if pd.notna(event_type) else "Earnings",
        })

    return {"data": rows}


def fetch_financial_health_chart(symbol: str) -> dict:
    bio_info = dh.get_symbol_bio_info(symbol)
    bio_fund_info = dh.get_symbol_fundamental_info(symbol)

    if not bio_info:
        return error_payload("No bio data found")
    if not bio_fund_info:
        return error_payload("No fundamental data found")

    company = bio_info.get("LongName") or symbol
    sector = bio_info.get("Sector")
    kpis = bio_fund_info.get("kpis", {})
    metrics = {
        "net_debt_ebitda": kpis.get("NetDebtEbitda"),
        "interest_coverage": kpis.get("InterestCoverageEbit"),
        "current_ratio": kpis.get("CurrentRatio"),
        "quick_ratio": kpis.get("QuickRatio"),
    }

    thresholds = {
        "nde_neutral": 0.0,
        "nde_strong": 1.0,
        "nde_very_strong": 3.0,
        "ic_weak": 3.0,
        "ic_neutral": 8.0,
    }

    payload = {
        "symbol": symbol,
        "company": company,
        "sector": sector or "Unknown",
        "metrics": metrics,
        "thresholds": thresholds,
        "asof": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "peers": build_financial_health_peers(symbol, limit=3),
    }
    return {"data": payload}


def fetch_profitability_chart(symbol: str) -> dict:
    bio_info = dh.get_symbol_bio_info(symbol)
    bio_fund_info = dh.get_symbol_fundamental_info_profitability(symbol)

    if not bio_info:
        return error_payload("No bio data found")
    if not bio_fund_info:
        return error_payload("No fundamental data found")

    series = bio_fund_info.get("series")
    if not isinstance(series, dict) or not series:
        return error_payload("No series data found")

    payload = {
        "symbol": symbol,
        "series": bio_fund_info.get("series", {}),
        "series_fy": bio_fund_info.get("series_fy", {}),
        "series_quarter": bio_fund_info.get("series_quarter", {}),
        "asof": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "peers": [],
    }
    return {"data": payload}


def fetch_efficiency_chart(symbol: str) -> dict:
    bio_info = dh.get_symbol_bio_info(symbol)
    cap_eff = dh.get_symbol_fundamental_info_capefficiency(symbol)

    if not bio_info:
        return error_payload("No bio data found")
    if not cap_eff:
        return error_payload("No fundamental data found")

    series_fy = cap_eff.get("series_fy", {})
    if not isinstance(series_fy, dict) or not series_fy.get("labels"):
        return error_payload("No FY series data found")

    payload = {
        "symbol": symbol,
        "series_fy": series_fy,
        "asof": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "peers": [],
    }
    return {"data": payload}
