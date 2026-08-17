import json

import numpy as np
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import render

from backend.datasources.yahoodata import DataHistoryYahoo
from frontend_app.decorators import login_required_api
from frontend_app.http_responses import df_to_excel_response
from frontend_app.services import screener_cache
from frontend_app.services import stock_data
from frontend_app.services import technical_metrics
from frontend_app.services.stock_summary import build_stock_summary
from frontend_app.symbols import normalize_symbol, validate_symbol
from frontend_app.view_helpers import (
    missing_symbol_response,
    provider_error_response,
    server_error_response,
)

dh = DataHistoryYahoo()


def _validated_symbol(symbol: str) -> str:
    normalized = normalize_symbol(symbol)
    if not normalized:
        raise ValueError("missing")
    return validate_symbol(normalized)


def _json_or_error(payload: dict, *, not_found_status: int = 404):
    if isinstance(payload, dict) and "error" in payload:
        return JsonResponse(payload, status=not_found_status)
    return JsonResponse(payload)


def _symbol_endpoint(symbol: str, handler, *, provider_message: str | None = None):
    try:
        validated = _validated_symbol(symbol)
    except ValueError:
        return missing_symbol_response()
    except Http404:
        raise

    try:
        return handler(validated)
    except ConnectionError:
        return provider_error_response(provider_message or "Failed to connect to Yahoo Finance API")
    except Exception as exc:
        return server_error_response(exc)


# ------------------------- Pages -------------------------
def home(request):
    return render(request, "index.html")


@login_required
def stockbytop_page(request):
    return render(request, "stockbytop.html")


def stock_page(request, symbol: str):
    return render(request, "stock.html", {"symbol": symbol})


def economic_calendar_page(request):
    return render(request, "economiccalendar.html")


# ------------------------- Market data -------------------------
def get_dh(request, symbol: str):
    try:
        validated = _validated_symbol(symbol)
        period = request.GET.get("period", "1mo")
        interval = request.GET.get("interval", "1d")
        payload = stock_data.fetch_data_history(validated, period=period, interval=interval)
        if "_df" in payload:
            payload.pop("_df")
        if "error" in payload:
            return JsonResponse(payload, status=404)
        return JsonResponse(payload)
    except ValueError:
        return missing_symbol_response()
    except Http404:
        raise
    except Exception as exc:
        return server_error_response(exc)


@login_required_api
def get_stock_gainers(request):
    df = screener_cache.get_or_fetch_screener("gainers")
    if df is None or df.empty:
        return JsonResponse({"error": "No data found"}, status=404)
    return JsonResponse({"data": df.to_dict(orient="records")})


@login_required_api
def get_stock_trending(request):
    try:
        df = screener_cache.get_or_fetch_screener("trending")
        if df is None or df.empty:
            return JsonResponse({"error": "No data found"}, status=404)
        return JsonResponse({"data": df.to_dict(orient="records")})
    except ConnectionError:
        return provider_error_response("Failed to connect to Provider API")
    except Exception as exc:
        return server_error_response(exc)


@login_required_api
def get_stock_most_active(request):
    try:
        df = screener_cache.get_or_fetch_screener("most_active")
        if df is None or df.empty:
            return JsonResponse({"error": "No data found"}, status=404)
        return JsonResponse({"data": df.to_dict(orient="records")})
    except ConnectionError:
        return provider_error_response("Failed to connect to Provider API")
    except Exception as exc:
        return server_error_response(exc)


# ------------------------- Technical metrics -------------------------
def get_crossover_trend_metrics(request, symbol: str):
    def handler(validated: str):
        try:
            fastperiod = int(request.GET.get("fast", 5))
            mediumperiod = int(request.GET.get("medium", 10))
            slowperiod = int(request.GET.get("slow", 20))
            if fastperiod <= 0 or mediumperiod <= 0 or slowperiod <= 0:
                return JsonResponse({"error": "Periods must be positive integers."}, status=400)
            if not (fastperiod < mediumperiod < slowperiod):
                return JsonResponse({"error": "Fast < Medium < Slow periods required."}, status=400)
        except ValueError:
            return JsonResponse({"error": "Periods must be valid integers."}, status=400)

        raw_data = request.GET.get("data")
        if raw_data:
            try:
                data_list = technical_metrics.parse_json_records(raw_data)
                if len(data_list) < slowperiod:
                    return JsonResponse({"error": "Not enough data for moving average calculation."}, status=400)
                close_prices = technical_metrics.close_prices_from_records(data_list)
                if np.isnan(close_prices).any():
                    return JsonResponse({"error": "Invalid data: missing Close prices."}, status=400)
            except (json.JSONDecodeError, KeyError, TypeError) as exc:
                return JsonResponse({"error": f"Invalid data format: {str(exc)}"}, status=400)
        else:
            df = stock_data.get_history_dataframe(validated, period="1mo", interval="1d")
            if df is None:
                return JsonResponse({"error": "No data found"}, status=404)
            close_prices = df["Close"].to_numpy(dtype=np.float64)

        result = technical_metrics.crossover_from_prices(
            validated, close_prices, fastperiod, mediumperiod, slowperiod
        )
        return JsonResponse(result)

    try:
        return _symbol_endpoint(symbol, handler)
    except Http404:
        raise
    except Exception as exc:
        return server_error_response(exc)


def get_crossover_trend_metrics_draw(request, symbol: str):
    def handler(validated: str):
        fast = int(request.GET.get("fast", 14))
        medium = int(request.GET.get("medium", 25))
        slow = int(request.GET.get("slow", 200))
        result = technical_metrics.draw_crossover_history(validated, fast, medium, slow)
        if "error" in result:
            return JsonResponse(result, status=404)
        return JsonResponse(result)

    return _symbol_endpoint(symbol, handler)


def get_adx_trend_metrics(request, symbol: str):
    def handler(validated: str):
        try:
            length = int(request.GET.get("length", 5))
            if length <= 0:
                return JsonResponse({"error": "Length must be a positive integer."}, status=400)
        except ValueError:
            return JsonResponse({"error": "Length must be an integer."}, status=400)

        raw_data = request.GET.get("data")
        if raw_data:
            try:
                data_list = technical_metrics.parse_json_records(raw_data)
                if len(data_list) < length:
                    return JsonResponse({"error": "Not enough data for ADX calculation."}, status=400)
                _, high_prices, low_prices, close_prices, _ = technical_metrics.ohlc_arrays_from_records(data_list)
                if np.isnan(close_prices).any() or np.isnan(high_prices).any() or np.isnan(low_prices).any():
                    return JsonResponse({"error": "Invalid data: missing Close, High, or Low prices."}, status=400)
            except (json.JSONDecodeError, KeyError, TypeError) as exc:
                return JsonResponse({"error": f"Invalid data format: {str(exc)}"}, status=400)
        else:
            df = stock_data.get_history_dataframe(validated, period="1mo", interval="1d")
            if df is None:
                return JsonResponse({"error": "No data found"}, status=404)
            close_prices = df["Close"].to_numpy(dtype=np.float64)
            high_prices = df["High"].to_numpy(dtype=np.float64)
            low_prices = df["Low"].to_numpy(dtype=np.float64)

        result = technical_metrics.adx_from_prices(validated, high_prices, low_prices, close_prices, length)
        return JsonResponse(result)

    return _symbol_endpoint(symbol, handler)


def get_bollinger_bands_metrics(request, symbol: str):
    def handler(validated: str):
        try:
            length = int(request.GET.get("length", 5))
            std_dev = int(request.GET.get("std_dev", 5))
            if length <= 0 or std_dev <= 0:
                return JsonResponse({"error": "Length and Standard Deviation must be positive integers."}, status=400)
        except ValueError:
            return JsonResponse({"error": "Length and std_dev must be integers."}, status=400)

        raw_data = request.GET.get("data")
        if raw_data:
            try:
                data_list = technical_metrics.parse_json_records(raw_data)
                if len(data_list) < length:
                    return JsonResponse({"error": "Not enough data for SMA calculation."}, status=400)
                close_prices = technical_metrics.close_prices_from_records(data_list)
                if np.isnan(close_prices).any():
                    return JsonResponse({"error": "Invalid data: missing Close prices."}, status=400)
            except (json.JSONDecodeError, KeyError, TypeError) as exc:
                return JsonResponse({"error": f"Invalid data format: {str(exc)}"}, status=400)
        else:
            df = stock_data.get_history_dataframe(validated, period="1mo", interval="1d")
            if df is None:
                return JsonResponse({"error": "No data found"}, status=404)
            close_prices = df["Close"].to_numpy(dtype=np.float64)

        result = technical_metrics.bollinger_from_prices(validated, close_prices, length, std_dev)
        return JsonResponse(result)

    return _symbol_endpoint(symbol, handler)


def get_bollinger_bands_metrics_draw(request, symbol: str):
    def handler(validated: str):
        length = int(request.GET.get("length", 14))
        std = int(request.GET.get("std", 2))
        result = technical_metrics.draw_bollinger_history(validated, length, std)
        if "error" in result:
            return JsonResponse(result, status=404)
        return JsonResponse(result)

    return _symbol_endpoint(symbol, handler)


def get_rsi_trend_metrics(request, symbol: str):
    def handler(validated: str):
        try:
            length = int(request.GET.get("length", 5))
            upper_level = int(request.GET.get("upper_level", 5))
            lower_level = int(request.GET.get("lower_level", 5))
            if length <= 0 or upper_level <= lower_level:
                return JsonResponse({"error": "Invalid parameter values."}, status=400)
        except ValueError:
            return JsonResponse({"error": "Length, Upper Level and Lower Level must by integers."}, status=400)

        raw_data = request.GET.get("data")
        if raw_data:
            try:
                data_list = technical_metrics.parse_json_records(raw_data)
                close_prices = np.array(
                    [entry["Close"] for entry in data_list if "Close" in entry], dtype=np.float64
                )
            except (json.JSONDecodeError, KeyError, TypeError) as exc:
                return JsonResponse({"error": f"Invalid data format: {str(exc)}"}, status=400)
        else:
            df = stock_data.get_history_dataframe(validated, period="1mo", interval="1d")
            if df is None:
                return JsonResponse({"error": "No data found"}, status=404)
            close_prices = df["Close"].to_numpy(dtype=np.float64)

        result = technical_metrics.rsi_from_prices(validated, close_prices, length, upper_level, lower_level)
        return JsonResponse(result)

    return _symbol_endpoint(symbol, handler)


def get_rsi_trend_metrics_draw(request, symbol: str):
    def handler(validated: str):
        upper_level = int(request.GET.get("upper_level", 70))
        lower_level = int(request.GET.get("lower_level", 30))
        length = int(request.GET.get("length", 30))
        result = technical_metrics.draw_rsi_history(validated, length, upper_level, lower_level)
        if "error" in result:
            return JsonResponse(result, status=404)
        return JsonResponse(result)

    return _symbol_endpoint(symbol, handler)


def get_candle_detection(request, symbol: str):
    def handler(validated: str):
        raw_data = request.GET.get("data")
        if raw_data:
            try:
                data_list = technical_metrics.parse_json_records(raw_data)
                if len(data_list) < 5:
                    return JsonResponse({"error": "Not enough data for pattern detection."}, status=400)
                open_prices, high_prices, low_prices, close_prices, dates = (
                    technical_metrics.ohlc_arrays_from_records(data_list)
                )
                if np.isnan(close_prices).any() or np.isnan(open_prices).any():
                    return JsonResponse({"error": "Invalid data: missing Close or Open prices."}, status=400)
            except (json.JSONDecodeError, KeyError, TypeError) as exc:
                return JsonResponse({"error": f"Invalid data format: {str(exc)}"}, status=400)
            result = technical_metrics.candle_patterns_from_arrays(
                validated, open_prices, high_prices, low_prices, close_prices, dates
            )
        else:
            df = stock_data.get_history_dataframe(validated, period="3mo", interval="1d")
            if df is None:
                return JsonResponse({"error": "No data found"}, status=404)
            result = technical_metrics.compute_candle_patterns(validated, df)

        return JsonResponse(result)

    return _symbol_endpoint(symbol, handler)


def get_harmonic_patterns(request, symbol: str):
    def handler(validated: str):
        raw_data = request.GET.get("data")
        if raw_data:
            try:
                data_list = technical_metrics.parse_json_records(raw_data)
                if len(data_list) < 5:
                    return JsonResponse({"error": "Not enough data for pattern detection."}, status=400)
                df = technical_metrics.records_to_dataframe(data_list)
            except (json.JSONDecodeError, KeyError, TypeError) as exc:
                return JsonResponse({"error": f"Invalid data format: {str(exc)}"}, status=400)
        else:
            df = stock_data.get_history_dataframe(validated, period="1mo", interval="1d")
            if df is None:
                return JsonResponse({"error": "No data found"}, status=404)

        result = technical_metrics.harmonic_patterns_from_dataframe(df)
        return JsonResponse(result)

    return _symbol_endpoint(symbol, handler)


# ------------------------- Fundamentals & holders -------------------------
def get_inst_holders(request, symbol: str):
    def handler(validated: str):
        return _json_or_error(stock_data.fetch_institutional_holders(validated))

    return _symbol_endpoint(symbol, handler)


def get_inside_transactions(request, symbol: str):
    def handler(validated: str):
        return _json_or_error(stock_data.fetch_inside_transactions(validated))

    return _symbol_endpoint(symbol, handler)


def get_recommendations(request, symbol: str):
    def handler(validated: str):
        return _json_or_error(stock_data.fetch_recommendations(validated))

    return _symbol_endpoint(symbol, handler)


def get_fundamental_info(request, symbol: str):
    def handler(validated: str):
        return _json_or_error(stock_data.fetch_fundamental_info(validated))

    return _symbol_endpoint(symbol, handler)


def get_fundamental_evaluations(request, symbol: str):
    def handler(validated: str):
        return _json_or_error(stock_data.fetch_fundamental_evaluations(validated))

    return _symbol_endpoint(symbol, handler)


def _fundamental_download(handler, symbol: str, filename: str):
    def inner(validated: str):
        return df_to_excel_response(handler(validated), filename.format(symbol=validated))

    return _symbol_endpoint(symbol, inner)


def get_fundamental_income_download(request, symbol: str):
    return _fundamental_download(dh.get_yahoo_symbol_income, symbol, "{symbol}_income_statement")


def get_fundamental_balance_sheet_download(request, symbol: str):
    return _fundamental_download(dh.get_yahoo_symbol_balance_sheet, symbol, "{symbol}_balance_sheet")


def get_fundamental_cashflow_download(request, symbol: str):
    return _fundamental_download(dh.get_yahoo_symbol_cashflow, symbol, "{symbol}_cashflow")


def get_fundamental_income_quarterly_download(request, symbol: str):
    return _fundamental_download(
        dh.get_yahoo_symbol_income_quarterly, symbol, "{symbol}_income_stmt_quarterly"
    )


def get_fundamental_balance_sheet_quarterly_download(request, symbol: str):
    return _fundamental_download(
        dh.get_yahoo_symbol_balance_sheet_quarterly, symbol, "{symbol}_balance_sheet_quarterly"
    )


def get_fundamental_cashflow_quarterly_download(request, symbol: str):
    return _fundamental_download(
        dh.get_yahoo_symbol_cashflow_quarterly, symbol, "{symbol}_cashflow_quarterly"
    )


def get_bio_info(request, symbol: str):
    def handler(validated: str):
        return _json_or_error(stock_data.fetch_bio(validated))

    return _symbol_endpoint(symbol, handler)


def get_symbol_fundamental_news(request, symbol: str):
    def handler(validated: str):
        return _json_or_error(stock_data.fetch_news(validated))

    return _symbol_endpoint(symbol, handler)


def get_yahoo_symbol_earnings_dates(request, symbol: str):
    def handler(validated: str):
        return JsonResponse(stock_data.fetch_earnings_dates(validated), status=200)

    return _symbol_endpoint(symbol, handler)


def get_financial_health_chart_info(request, symbol: str):
    def handler(validated: str):
        payload = stock_data.fetch_financial_health_chart(validated)
        if "error" in payload:
            return JsonResponse(payload, status=404)
        return JsonResponse(payload, status=200)

    return _symbol_endpoint(symbol, handler)


def get_profitability_chart_info(request, symbol: str):
    def handler(validated: str):
        payload = stock_data.fetch_profitability_chart(validated)
        if "error" in payload:
            return JsonResponse(payload, status=404)
        return JsonResponse(payload, status=200)

    return _symbol_endpoint(symbol, handler)


def get_efficiency_chart_info(request, symbol: str):
    def handler(validated: str):
        payload = stock_data.fetch_efficiency_chart(validated)
        if "error" in payload:
            return JsonResponse(payload, status=404)
        return JsonResponse(payload, status=200)

    return _symbol_endpoint(symbol, handler)


def get_pivot_points(request, symbol: str):
    def handler(validated: str):
        method = request.GET.get("method", technical_metrics.DEFAULT_PIVOT_METHOD).lower()
        df = stock_data.get_history_dataframe(validated, period="3mo", interval="1d")
        if df is None:
            return JsonResponse({"error": "No data found"}, status=404)
        result = technical_metrics.compute_pivot_points(validated, df, method=method)
        if "error" in result:
            status = 400 if "Invalid method" in result["error"] else 404
            return JsonResponse(result, status=status)
        return JsonResponse(result)

    return _symbol_endpoint(symbol, handler)


def get_stock_summary(request, symbol: str):
    try:
        validated = _validated_symbol(symbol)
        portfolio_value = None
        risk_percent = None
        if request.user.is_authenticated:
            portfolio_value = float(request.user.portfolio_value)
            risk_percent = float(request.user.risk_percent)
        summary = build_stock_summary(
            validated,
            portfolio_value=portfolio_value,
            risk_percent=risk_percent,
        )
        return JsonResponse(summary)
    except ValueError:
        return missing_symbol_response()
    except Http404:
        raise
    except Exception as exc:
        return server_error_response(exc)
