import json

import numpy as np
import pandas as pd

from backend.tecnical_analysis.candlestick_chart_data import CandlestickData
from backend.tecnical_analysis.candles_patterns import CandlesPatterns
from backend.tecnical_analysis.harmonic_patterns import HarmonicPatterns
from backend.tecnical_analysis.pivot_points import SUPPORTED_METHODS, calculate_levels, pivot_signal
from backend.tecnical_analysis.trend_metrics import TrendMetrics

from frontend_app.services.stock_data import get_history_dataframe

# Defaults aligned with static/js/api.js initial page load
DEFAULT_CROSSOVER = (14, 25, 200)
DEFAULT_ADX_LENGTH = 14
DEFAULT_BOLLINGER = (14, 2)
DEFAULT_RSI = (14, 70, 30)


def tail_df(df: pd.DataFrame | None, rows: int) -> pd.DataFrame | None:
    if df is None or df.empty:
        return df
    return df.tail(rows).copy()


def compute_crossover(
    symbol: str,
    df: pd.DataFrame,
    fast: int | None = None,
    medium: int | None = None,
    slow: int | None = None,
) -> dict:
    fastperiod, mediumperiod, slowperiod = DEFAULT_CROSSOVER if fast is None else (fast, medium, slow)
    close_prices = df["Close"].to_numpy(dtype=np.float64)
    tm = TrendMetrics()
    return tm.get_crossover(close_prices, symbol, fastperiod, mediumperiod, slowperiod)


def compute_adx(symbol: str, df: pd.DataFrame, length: int | None = None) -> dict:
    adx_length = DEFAULT_ADX_LENGTH if length is None else length
    close_prices = df["Close"].to_numpy(dtype=np.float64)
    high_prices = df["High"].to_numpy(dtype=np.float64)
    low_prices = df["Low"].to_numpy(dtype=np.float64)
    tm = TrendMetrics()
    return tm.get_adx(high_prices, low_prices, close_prices, symbol, adx_length)


def compute_bollinger(
    symbol: str,
    df: pd.DataFrame,
    length: int | None = None,
    std_dev: int | None = None,
) -> dict:
    band_length, band_std = DEFAULT_BOLLINGER if length is None else (length, std_dev)
    close_prices = df["Close"].to_numpy(dtype=np.float64)
    tm = TrendMetrics()
    return tm.get_bollinger_bands(symbol, close_prices, band_length, band_std)


def compute_rsi(
    symbol: str,
    df: pd.DataFrame,
    length: int | None = None,
    upper: int | None = None,
    lower: int | None = None,
) -> dict:
    rsi_length, upper_level, lower_level = DEFAULT_RSI if length is None else (length, upper, lower)
    close_prices = df["Close"].to_numpy(dtype=np.float64)
    tm = TrendMetrics()
    return tm.get_rsi(symbol, close_prices, rsi_length, upper_level, lower_level)


def compute_candle_patterns(symbol: str, df: pd.DataFrame) -> dict:
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


def compute_harmonic_patterns(df: pd.DataFrame) -> dict:
    hp = HarmonicPatterns()
    result = hp.backtest_harmonic_patterns(
        data=df,
        err_allowed=0.02,
        order=5,
        stop_factor=0.1,
        future_window=20,
    )
    return {"patterns_detected": result}


def crossover_from_prices(
    symbol: str,
    close_prices: np.ndarray,
    fast: int,
    medium: int,
    slow: int,
) -> dict:
    tm = TrendMetrics()
    return tm.get_crossover(close_prices, symbol, fast, medium, slow)


def adx_from_prices(
    symbol: str,
    high_prices: np.ndarray,
    low_prices: np.ndarray,
    close_prices: np.ndarray,
    length: int,
) -> dict:
    tm = TrendMetrics()
    return tm.get_adx(high_prices, low_prices, close_prices, symbol, length)


def bollinger_from_prices(
    symbol: str,
    close_prices: np.ndarray,
    length: int,
    std_dev: int,
) -> dict:
    tm = TrendMetrics()
    return tm.get_bollinger_bands(symbol, close_prices, length, std_dev)


def rsi_from_prices(
    symbol: str,
    close_prices: np.ndarray,
    length: int,
    upper_level: int,
    lower_level: int,
) -> dict:
    tm = TrendMetrics()
    return tm.get_rsi(symbol, close_prices, length, upper_level, lower_level)


def candle_patterns_from_arrays(
    symbol: str,
    open_prices: np.ndarray,
    high_prices: np.ndarray,
    low_prices: np.ndarray,
    close_prices: np.ndarray,
    dates: np.ndarray,
) -> dict:
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


def harmonic_patterns_from_dataframe(df: pd.DataFrame) -> dict:
    return compute_harmonic_patterns(df)


def draw_crossover_history(symbol: str, fast: int, medium: int, slow: int) -> dict:
    df = get_history_dataframe(symbol, period="1y", interval="1d")
    if df is None:
        return {"error": "Sem dados"}

    cd = CandlestickData()
    result = cd.get_ema_history(df, fast, medium, slow)
    result["symbol"] = symbol.upper()
    return result


def draw_bollinger_history(symbol: str, length: int, std: int) -> dict:
    df = get_history_dataframe(symbol, period="1y", interval="1d")
    if df is None:
        return {"error": "Sem dados"}

    cd = CandlestickData()
    result = cd.get_bollinger_bands_history(df, length, std)
    result["symbol"] = symbol.upper()
    return result


def draw_rsi_history(symbol: str, length: int, upper_level: int, lower_level: int) -> dict:
    df = get_history_dataframe(symbol, period="1y", interval="1d")
    if df is None:
        return {"error": "Sem dados"}

    cd = CandlestickData()
    result = cd.get_rsi_history(df, length, upper_level, lower_level)
    result["symbol"] = symbol.upper()
    return result


def parse_json_records(raw_data: str) -> list[dict]:
    return json.loads(raw_data)


def ohlc_arrays_from_records(data_list: list[dict]) -> tuple[np.ndarray, ...]:
    close_prices = np.array([entry["Close"] for entry in data_list if "Close" in entry], dtype=np.float64)
    high_prices = np.array([entry["High"] for entry in data_list if "High" in entry], dtype=np.float64)
    low_prices = np.array([entry["Low"] for entry in data_list if "Low" in entry], dtype=np.float64)
    open_prices = np.array([entry["Open"] for entry in data_list if "Open" in entry], dtype=np.float64)
    dates = np.array([entry["Date"] for entry in data_list if "Date" in entry])
    return open_prices, high_prices, low_prices, close_prices, dates


def close_prices_from_records(data_list: list[dict]) -> np.ndarray:
    return np.array([entry.get("Close", np.nan) for entry in data_list], dtype=np.float64)


DEFAULT_PIVOT_METHOD = "classic"


def compute_pivot_points(
    symbol: str,
    df: pd.DataFrame,
    method: str = DEFAULT_PIVOT_METHOD,
) -> dict:
    if method not in SUPPORTED_METHODS:
        return {"error": f"Invalid method. Use one of: {', '.join(SUPPORTED_METHODS)}"}

    if df is None or len(df) < 2:
        return {"error": "Not enough data for pivot calculation"}

    reference = df.iloc[-2]
    current = df.iloc[-1]

    try:
        high = float(reference["High"])
        low = float(reference["Low"])
        close = float(reference["Close"])
        current_price = float(current["Close"])
    except (KeyError, TypeError, ValueError):
        return {"error": "Invalid OHLC data for pivot calculation"}

    levels = calculate_levels(high, low, close, method)
    rounded_levels = {key: round(value, 4) for key, value in levels.items()}

    reference_date = reference["Date"] if "Date" in reference else None
    if hasattr(reference_date, "isoformat"):
        reference_date = reference_date.isoformat()
    elif reference_date is not None:
        reference_date = str(reference_date)

    return {
        "symbol": symbol,
        "method": method,
        "reference_date": reference_date,
        "reference_ohlc": {
            "high": round(high, 4),
            "low": round(low, 4),
            "close": round(close, 4),
        },
        "current_price": round(current_price, 4),
        "levels": rounded_levels,
        "signal": pivot_signal(current_price, levels),
    }


def records_to_dataframe(data_list: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(data_list)
