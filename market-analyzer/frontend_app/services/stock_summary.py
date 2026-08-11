from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd

from backend.datasources.yahoodata import DataHistoryYahoo
from backend.risk_manager.risk_manager import RiskManagerFundamental
from backend.tecnical_analysis.candles_patterns import CandlesPatterns
from backend.tecnical_analysis.harmonic_patterns import HarmonicPatterns
from backend.tecnical_analysis.trend_metrics import TrendMetrics
from frontend_app.services.decision_verdict import build_decision_verdict

dh = DataHistoryYahoo()

# Defaults aligned with static/js/api.js initial page load
DEFAULT_CROSSOVER = (14, 25, 200)
DEFAULT_ADX_LENGTH = 14
DEFAULT_BOLLINGER = (14, 2)
DEFAULT_RSI = (14, 70, 30)


def _error(message: str) -> dict:
    return {"error": message}


def _tail_df(df: pd.DataFrame | None, rows: int) -> pd.DataFrame | None:
    if df is None or df.empty:
        return df
    return df.tail(rows).copy()


def _fetch_bio(symbol: str) -> dict:
    bio_info = dh.get_symbol_bio_info(symbol)
    if not bio_info:
        return _error("No data found")
    bio_info = {k: (None if v == "N/A" else v) for k, v in bio_info.items()}
    return {"data": bio_info}


def _fetch_news(symbol: str) -> dict:
    news = dh.get_yahoo_symbol_news(symbol)
    if not news:
        return _error("No data found")
    return {"data": news}


def _fetch_data_history(symbol: str, period: str = "1y", interval: str = "1d") -> dict:
    df = dh.get_data_history(symbol=symbol, period=period, interval=interval)
    if df is None or df.empty:
        return _error("No data found")
    return {"data": df.to_dict(orient="records"), "_df": df}


def _fetch_inside_transactions(symbol: str) -> dict:
    df = dh.get_symbol_inside_transactions(symbol)
    if df is None or df.empty:
        return _error("No data found")

    df = df.copy()
    df["StartDate"] = (
        pd.to_datetime(df["StartDate"], utc=True)
        .dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    )
    df["Shares"] = pd.to_numeric(df["Shares"], errors="coerce")
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
    df = df.replace({np.nan: None})
    return {"data": df.to_dict(orient="records")}


def _fetch_fundamentals(symbol: str) -> dict:
    raw = dh.get_symbol_fundamental_info(symbol)
    if not raw:
        err = _error("No data found")
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


def _compute_crossover(symbol: str, df: pd.DataFrame) -> dict:
    fast, medium, slow = DEFAULT_CROSSOVER
    close_prices = df["Close"].to_numpy(dtype=np.float64)
    tm = TrendMetrics()
    return tm.get_crossover(close_prices, symbol, fast, medium, slow)


def _compute_adx(symbol: str, df: pd.DataFrame) -> dict:
    close_prices = df["Close"].to_numpy(dtype=np.float64)
    high_prices = df["High"].to_numpy(dtype=np.float64)
    low_prices = df["Low"].to_numpy(dtype=np.float64)
    tm = TrendMetrics()
    return tm.get_adx(high_prices, low_prices, close_prices, symbol, DEFAULT_ADX_LENGTH)


def _compute_bollinger(symbol: str, df: pd.DataFrame) -> dict:
    length, std_dev = DEFAULT_BOLLINGER
    close_prices = df["Close"].to_numpy(dtype=np.float64)
    tm = TrendMetrics()
    return tm.get_bollinger_bands(symbol, close_prices, length, std_dev)


def _compute_rsi(symbol: str, df: pd.DataFrame) -> dict:
    length, upper, lower = DEFAULT_RSI
    close_prices = df["Close"].to_numpy(dtype=np.float64)
    tm = TrendMetrics()
    return tm.get_rsi(symbol, close_prices, length, upper, lower)


def _compute_candle_patterns(symbol: str, df: pd.DataFrame) -> dict:
    close_prices = df["Close"].to_numpy(dtype=np.float64)
    low_prices = df["Low"].to_numpy(dtype=np.float64)
    high_prices = df["High"].to_numpy(dtype=np.float64)
    open_prices = df["Open"].to_numpy(dtype=np.float64)
    dates = df["Date"].to_numpy()

    cp = CandlesPatterns()
    detected_patterns = {}

    for method_name in dir(cp):
        if method_name.startswith("_") or method_name == "detect_pattern":
            continue

        pattern_func = getattr(cp, method_name)
        if not callable(pattern_func):
            continue

        try:
            detection_result = pattern_func(
                {
                    "Open": open_prices,
                    "High": high_prices,
                    "Low": low_prices,
                    "Close": close_prices,
                },
                dates,
            )
            if isinstance(detection_result, list) and detection_result:
                detected_patterns[method_name] = detection_result[-5:]
        except Exception as exc:
            detected_patterns[method_name] = f"Error processing pattern: {str(exc)}"

    if not detected_patterns:
        return {"symbol": symbol, "patterns_detected": "No patterns found"}

    return {"symbol": symbol, "patterns_detected": detected_patterns}


def _compute_harmonic_patterns(df: pd.DataFrame) -> dict:
    hp = HarmonicPatterns()
    result = hp.backtest_harmonic_patterns(
        data=df,
        err_allowed=0.02,
        order=5,
        stop_factor=0.1,
        future_window=20,
    )
    return {"patterns_detected": result}


def _run_section(name: str, fn) -> tuple[str, dict]:
    try:
        return name, fn()
    except ConnectionError:
        return name, _error("Failed to connect to Provider API")
    except Exception as exc:
        return name, _error(str(exc))


def build_stock_summary(symbol: str) -> dict:
    summary = {"symbol": symbol}

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(_run_section, "bio", lambda: _fetch_bio(symbol)),
            executor.submit(_run_section, "news", lambda: _fetch_news(symbol)),
            executor.submit(
                _run_section,
                "data_history",
                lambda: _fetch_data_history(symbol, period="1y", interval="1d"),
            ),
            executor.submit(_run_section, "fundamentals", lambda: _fetch_fundamentals(symbol)),
            executor.submit(
                _run_section,
                "inside_transactions",
                lambda: _fetch_inside_transactions(symbol),
            ),
        ]

        history_df = None
        for future in futures:
            key, payload = future.result()
            if key == "data_history" and isinstance(payload, dict) and "_df" in payload:
                history_df = payload.pop("_df")
            elif key == "fundamentals" and isinstance(payload, dict):
                if "fundamental_info" in payload:
                    summary["fundamental_info"] = payload["fundamental_info"]
                    summary["fundamental_evaluations"] = payload["fundamental_evaluations"]
                else:
                    summary["fundamental_info"] = payload
                    summary["fundamental_evaluations"] = payload
                continue
            summary[key] = payload

    if history_df is not None and not history_df.empty:
        ta_df = history_df
        candles_df = _tail_df(history_df, 63)

        ta_sections = {
            "crossover": lambda: _compute_crossover(symbol, ta_df),
            "adx": lambda: _compute_adx(symbol, _tail_df(history_df, 30) or ta_df),
            "bollinger": lambda: _compute_bollinger(symbol, _tail_df(history_df, 30) or ta_df),
            "rsi": lambda: _compute_rsi(symbol, _tail_df(history_df, 30) or ta_df),
            "harmonic_patterns": lambda: _compute_harmonic_patterns(_tail_df(history_df, 30) or ta_df),
        }

        if candles_df is not None and not candles_df.empty:
            ta_sections["candle_patterns"] = lambda: _compute_candle_patterns(symbol, candles_df)

        with ThreadPoolExecutor(max_workers=len(ta_sections)) as executor:
            ta_futures = [
                executor.submit(_run_section, name, fn)
                for name, fn in ta_sections.items()
            ]
            for future in ta_futures:
                key, payload = future.result()
                summary[key] = payload
    else:
        for key in (
            "crossover",
            "adx",
            "bollinger",
            "rsi",
            "candle_patterns",
            "harmonic_patterns",
        ):
            summary.setdefault(key, _error("No data found"))

    summary.setdefault("fundamental_info", _error("No data found"))
    summary.setdefault("fundamental_evaluations", _error("No data found"))

    summary["verdict"] = build_decision_verdict(
        symbol=symbol,
        fundamental_info=summary.get("fundamental_info"),
        fundamental_evaluations=summary.get("fundamental_evaluations"),
        crossover=summary.get("crossover"),
        adx=summary.get("adx"),
        bollinger=summary.get("bollinger"),
        rsi=summary.get("rsi"),
    )

    return summary
