from concurrent.futures import ThreadPoolExecutor

from frontend_app.services.decision_verdict import build_decision_verdict
from frontend_app.services import stock_data
from frontend_app.services import technical_metrics
from frontend_app.services.trade_plan import build_trade_plan


def _run_section(name: str, fn) -> tuple[str, dict]:
    try:
        return name, fn()
    except ConnectionError:
        return name, stock_data.error_payload("Failed to connect to Provider API")
    except Exception as exc:
        return name, stock_data.error_payload(str(exc))


def build_stock_summary(symbol: str, *, portfolio_value: float | None = None, risk_percent: float | None = None) -> dict:
    summary = {"symbol": symbol}

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(_run_section, "bio", lambda: stock_data.fetch_bio(symbol)),
            executor.submit(_run_section, "news", lambda: stock_data.fetch_news(symbol)),
            executor.submit(
                _run_section,
                "data_history",
                lambda: stock_data.fetch_data_history(symbol, period="1y", interval="1d"),
            ),
            executor.submit(_run_section, "fundamentals", lambda: stock_data.fetch_fundamentals(symbol)),
            executor.submit(
                _run_section,
                "inside_transactions",
                lambda: stock_data.fetch_inside_transactions(symbol),
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
        candles_df = technical_metrics.tail_df(history_df, 63)

        ta_sections = {
            "crossover": lambda: technical_metrics.compute_crossover(symbol, ta_df),
            "adx": lambda: technical_metrics.compute_adx(
                symbol, technical_metrics.tail_df(history_df, 30) or ta_df
            ),
            "bollinger": lambda: technical_metrics.compute_bollinger(
                symbol, technical_metrics.tail_df(history_df, 30) or ta_df
            ),
            "rsi": lambda: technical_metrics.compute_rsi(
                symbol, technical_metrics.tail_df(history_df, 30) or ta_df
            ),
            "harmonic_patterns": lambda: technical_metrics.compute_harmonic_patterns(
                technical_metrics.tail_df(history_df, 30) or ta_df
            ),
        }

        if candles_df is not None and not candles_df.empty:
            ta_sections["candle_patterns"] = lambda: technical_metrics.compute_candle_patterns(
                symbol, candles_df
            )

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
            summary.setdefault(key, stock_data.error_payload("No data found"))

    summary.setdefault("fundamental_info", stock_data.error_payload("No data found"))
    summary.setdefault("fundamental_evaluations", stock_data.error_payload("No data found"))

    summary["verdict"] = build_decision_verdict(
        symbol=symbol,
        fundamental_info=summary.get("fundamental_info"),
        fundamental_evaluations=summary.get("fundamental_evaluations"),
        crossover=summary.get("crossover"),
        adx=summary.get("adx"),
        bollinger=summary.get("bollinger"),
        rsi=summary.get("rsi"),
    )

    summary["trade_plan"] = build_trade_plan(
        symbol=symbol,
        verdict=summary["verdict"],
        bio=summary.get("bio"),
        harmonic_patterns=summary.get("harmonic_patterns"),
        candle_patterns=summary.get("candle_patterns"),
        bollinger=summary.get("bollinger"),
        portfolio_value=portfolio_value,
        risk_percent=risk_percent,
    )

    return summary
