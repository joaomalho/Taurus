import json
import numpy as np
import pandas as pd
from io import BytesIO
from datetime import datetime, timezone
from django.shortcuts import render
from django.utils.timezone import now
from django.http import JsonResponse, Http404, HttpResponse
from django.core.validators import RegexValidator
from backend.datasources.yahoodata import DataHistoryYahoo
from backend.tecnical_analysis.trend_metrics import TrendMetrics
from backend.tecnical_analysis.candlestick_chart_data import CandlestickData
from backend.tecnical_analysis.candles_patterns import CandlesPatterns
from backend.tecnical_analysis.harmonic_patterns import HarmonicPatterns
from backend.risk_manager.risk_manager import RiskManagerFundamental

dh = DataHistoryYahoo()


# ------------------------- Pages -------------------------
def home(request):
    return render(request, 'index.html')


# ------------------------- stockbytop Page -------------------------
def stockbytop_page(request):
    return render(request, 'stockbytop.html')


# ------------------------- Stock Pages -------------------------
def stock_page(request, symbol: str):
    return render(request, 'stock.html', {"symbol": symbol})


# ------------------------- Economic Calendar Pages -------------------------
def economic_calendar_page(request):
    return render(request, 'economiccalendar.html')


# ------------------------- Security Validations -------------------------
def validate_symbol(symbol):
    """
    Valida se o símbolo é uma string alfanumérica com no máximo 10 caracteres.
    """
    validator = RegexValidator(regex=r'^[A-Z0-9.]{1,10}$', message="Invalid symbol format.")
    try:
        validator(symbol)
        return symbol
    except Exception:
        raise Http404("Invalid stock symbol.")


def convert_numpy_types(obj):
    if isinstance(obj, (np.integer,)):
        return int(obj)
    elif isinstance(obj, (np.floating,)):
        return float(obj)
    elif isinstance(obj, (np.ndarray,)):
        return obj.tolist()
    elif isinstance(obj, (pd.Timestamp,)):
        return obj.isoformat()
    return obj


def _parse_iso_date(s: str):
    if not s:
        return None
    for fmt in ("%Y-%m-%d",):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    try:
        return datetime.fromisoformat(s).date()
    except ValueError:
        return None


def _df_to_excel_response(df, base_filename: str):

    if df is None or df.empty:
        return JsonResponse({"error": "No data found"}, status=404)

    # Melhorar layout: índice como coluna
    df_out = df.copy().reset_index().rename(columns={"index": "Period"})

    timestamp = now().strftime("%Y%m%d-%H%M")
    filename = f"{base_filename}_{timestamp}.xlsx"

    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df_out.to_excel(writer, index=False, sheet_name="Data")
    buffer.seek(0)

    response = HttpResponse(
        buffer.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


def get_dh(request, symbol: str):
    '''
    Data collection from yahoo

    Parameters:
    period : str
        Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max Either Use period parameter or use start and end
    interval : str
        Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo Intraday data cannot extend last 60 days
    start: str
        Download start date string (YYYY-MM-DD) or _datetime, inclusive. Default is 1900-01-01 E.g. for start="2020-01-01", the first data point will be on "2020-01-01"
    end: str
        Download end date string (YYYY-MM-DD) or _datetime, exclusive. Default is now E.g. for end="2023-01-01", the last data point will be on "2022-12-31"
    prepost : bool
        Include Pre and Post market data in results? Default is False
    '''
    try:
        symbol = symbol.strip().upper()

        if not symbol:
            return JsonResponse({"error": "Symbol is missing"}, status=400)

        symbol = validate_symbol(symbol)

        per = request.GET.get("period", "1mo")
        interval_time = request.GET.get("interval", "1d")

        try:
            df = dh.get_data_history(symbol=symbol, period=per, interval=interval_time)

            if df is None or df.empty:
                return JsonResponse({"error": "No data found"}, status=404)

            return JsonResponse({"data": df.to_dict(orient="records")})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    except Exception as e:
        return JsonResponse({"error": f"Unexpected server error: {str(e)}"}, status=500)


def get_stock_gainers(request):
    """
    View to pass Top 100 Gainers JSON.
    """

    df = dh.get_stocks_gainers()

    if df is None or df.empty:
        return JsonResponse({"error": "No data found"}, status=404)

    # Converte DataFrame para dicionário JSON
    return JsonResponse({"data": df.to_dict(orient="records")})


def get_stock_trending(request):
    """
    View to pass Top 100 Trending JSON.
    """
    try:
        df = dh.get_stocks_trending()

        if df is None or df.empty:
            return JsonResponse({"error": "No data found"}, status=404)

        # Converte DataFrame para dicionário JSON
        return JsonResponse({"data": df.to_dict(orient="records")})

    except ConnectionError:
        return JsonResponse({"error": "Failed to connect to Provider API"}, status=503)

    except Exception as e:
        return JsonResponse({"error": f"Unexpected server error: {str(e)}"}, status=500)


def get_stock_most_active(request):
    """
    View to pass Top 100 Most Active JSON.
    """
    try:
        df = dh.get_stocks_most_active()

        if df is None or df.empty:
            return JsonResponse({"error": "No data found"}, status=404)

        # Converte DataFrame para dicionário JSON
        return JsonResponse({"data": df.to_dict(orient="records")})

    except ConnectionError:
        return JsonResponse({"error": "Failed to connect to Provider API"}, status=503)

    except Exception as e:
        return JsonResponse({"error": f"Unexpected server error: {str(e)}"}, status=500)


def get_crossover_trend_metrics(request, symbol: str):
    """
    View to calculate crossover of 3 EMAs and return signals to frontend.
    """
    try:
        symbol = symbol.strip().upper()

        if not symbol:
            return JsonResponse({"error": "Symbol is missing"}, status=400)

        symbol = validate_symbol(symbol)

        try:
            fastperiod = int(request.GET.get("fast", 5))
            mediumperiod = int(request.GET.get("medium", 10))
            slowperiod = int(request.GET.get("slow", 20))

            # Garantindo que os valores sejam lógicos
            if fastperiod <= 0 or mediumperiod <= 0 or slowperiod <= 0:
                return JsonResponse({"error": "Periods must be positive integers."}, status=400)

            if not (fastperiod < mediumperiod < slowperiod):
                return JsonResponse({"error": "Fast < Medium < Slow periods required."}, status=400)

        except ValueError:
            return JsonResponse({"error": "Periods must be valid integers."}, status=400)

        raw_data = request.GET.get("data")

        if raw_data:
            try:
                data_list = json.loads(raw_data)

                # Validando se há dados suficientes para calcular cruzamento de médias
                if len(data_list) < slowperiod:
                    return JsonResponse({"error": "Not enough data for moving average calculation."}, status=400)

                close_prices = np.array([entry.get("Close", np.nan) for entry in data_list], dtype=np.float64)

                # Checando se há valores NaN nos dados
                if np.isnan(close_prices).any():
                    return JsonResponse({"error": "Invalid data: missing Close prices."}, status=400)

            except (json.JSONDecodeError, KeyError, TypeError) as e:
                return JsonResponse({"error": f"Invalid data format: {str(e)}"}, status=400)
        else:
            df = dh.get_data_history(symbol=symbol, period="1mo", interval="1d")

            if df is None or df.empty:
                return JsonResponse({"error": "No data found"}, status=404)

            close_prices = df["Close"].to_numpy(dtype=np.float64)

        tm = TrendMetrics()
        crossover_result = tm.get_crossover(close_prices, symbol, fastperiod, mediumperiod, slowperiod)

        return JsonResponse(crossover_result)

    except Exception as e:
        return JsonResponse({"error": f"Unexpected server error: {str(e)}"}, status=500)


def get_crossover_trend_metrics_draw(request, symbol: str):
    fast = int(request.GET.get("fast", 14))
    medium = int(request.GET.get("medium", 25))
    slow = int(request.GET.get("slow", 200))

    df = dh.get_data_history(symbol=symbol, period="1y", interval="1d")

    if df is None or df.empty:
        return JsonResponse({"error": "Sem dados"}, status=404)

    cd = CandlestickData()

    result = cd.get_ema_history(df, fast, medium, slow)
    result["symbol"] = symbol.upper()
    return JsonResponse(result)


def get_adx_trend_metrics(request, symbol: str):
    """
    View to calculate ADX and return signals to frontend.
    """
    try:
        symbol = symbol.strip().upper()

        if not symbol:
            return JsonResponse({"error": "Symbol is missing"}, status=400)

        symbol = validate_symbol(symbol)

        try:
            length = int(request.GET.get("length", 5))
            if length <= 0:
                return JsonResponse({"error": "Length must be a positive integer."}, status=400)
        except ValueError:
            return JsonResponse({"error": "Length must be an integer."}, status=400)

        raw_data = request.GET.get("data")

        if raw_data:
            try:
                data_list = json.loads(raw_data)

                # Validando se há dados suficientes para calcular ADX
                if len(data_list) < length:
                    return JsonResponse({"error": "Not enough data for ADX calculation."}, status=400)

                close_prices = np.array([entry["Close"] for entry in data_list if "Close" in entry], dtype=np.float64)
                high_prices = np.array([entry["High"] for entry in data_list if "High" in entry], dtype=np.float64)
                low_prices = np.array([entry["Low"] for entry in data_list if "Low" in entry], dtype=np.float64)

                # Checando se há valores NaN nos dados
                if np.isnan(close_prices).any() or np.isnan(high_prices).any() or np.isnan(low_prices).any():
                    return JsonResponse({"error": "Invalid data: missing Close, High, or Low prices."}, status=400)

            except (json.JSONDecodeError, KeyError, TypeError) as e:
                return JsonResponse({"error": f"Invalid data format: {str(e)}"}, status=400)
        else:
            df = dh.get_data_history(symbol=symbol, period="1mo", interval="1d")

            if df is None or df.empty:
                return JsonResponse({"error": "No data found"}, status=404)

            close_prices = df["Close"].to_numpy(dtype=np.float64)
            high_prices = df["High"].to_numpy(dtype=np.float64)
            low_prices = df["Low"].to_numpy(dtype=np.float64)

        tm = TrendMetrics()
        adx_result = tm.get_adx(high_prices, low_prices, close_prices, symbol, length)

        return JsonResponse(adx_result)

    except Exception as e:
        return JsonResponse({"error": f"Unexpected server error: {str(e)}"}, status=500)


def get_bollinger_bands_metrics(request, symbol: str):
    """
    View to calculate Bollinger Bands and return signals to frontend.
    """
    try:
        symbol = symbol.strip().upper()

        if not symbol:
            return JsonResponse({"error": "Symbol is missing"}, status=400)

        symbol = validate_symbol(symbol)

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
                data_list = json.loads(raw_data)
                # Garantindo que há dados suficientes para calcular SMA
                if len(data_list) < length:
                    return JsonResponse({"error": "Not enough data for SMA calculation."}, status=400)

                close_prices = np.array(
                    [entry.get("Close", np.nan) for entry in data_list], dtype=np.float64
                )

                if np.isnan(close_prices).any():
                    return JsonResponse({"error": "Invalid data: missing Close prices."}, status=400)

            except (json.JSONDecodeError, KeyError, TypeError) as e:
                return JsonResponse({"error": f"Invalid data format: {str(e)}"}, status=400)
        else:
            df = dh.get_data_history(symbol=symbol, period="1mo", interval="1d")

            if df is None or df.empty:
                return JsonResponse({"error": "No data found"}, status=404)

            close_prices = df["Close"].to_numpy(dtype=np.float64)

        tm = TrendMetrics()
        sma_bands_result = tm.get_bollinger_bands(symbol, close_prices, length, std_dev)

        return JsonResponse(sma_bands_result)

    except Exception as e:
        return JsonResponse({"error": f"Unexpected server error: {str(e)}"}, status=500)


def get_bollinger_bands_metrics_draw(request, symbol: str):
    length = int(request.GET.get("length", 14))
    std = int(request.GET.get("std", 2))

    df = dh.get_data_history(symbol=symbol, period="1y", interval="1d")

    if df is None or df.empty:
        return JsonResponse({"error": "Sem dados"}, status=404)

    cd = CandlestickData()

    result = cd.get_bollinger_bands_history(df, length, std)
    result["symbol"] = symbol.upper()
    return JsonResponse(result)


def get_rsi_trend_metrics(request, symbol: str):
    """
    View to calculate RSI and return signals to frontend.
    """
    try:
        symbol = symbol.strip().upper()
        if not symbol:
            return JsonResponse({"error": "Symbol is missing"}, status=400)

        symbol = validate_symbol(symbol)
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
                data_list = json.loads(raw_data)
                close_prices = np.array([entry["Close"] for entry in data_list if "Close" in entry], dtype=np.float64)
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                return JsonResponse({"error": f"Invalid data format: {str(e)}"}, status=400)
        else:
            df = dh.get_data_history(symbol=symbol, period="1mo", interval="1d")

            if df is None or df.empty:
                return JsonResponse({"error": "No data found"}, status=404)

            close_prices = df["Close"].to_numpy(dtype=np.float64)

        tm = TrendMetrics()
        rsi_result = tm.get_rsi(symbol, close_prices, length, upper_level, lower_level)

        return JsonResponse(rsi_result)

    except Exception as e:
        return JsonResponse({"error": f"Unexpected server error: {str(e)}"}, status=500)


def get_rsi_trend_metrics_draw(request, symbol: str):
    upper_level = int(request.GET.get("upper_level", 70))
    lower_level = int(request.GET.get("lower_level", 30))
    length = int(request.GET.get("length", 30))

    df = dh.get_data_history(symbol=symbol, period="1y", interval="1d")

    if df is None or df.empty:
        return JsonResponse({"error": "Sem dados"}, status=404)

    cd = CandlestickData()

    result = cd.get_rsi_history(df, length, upper_level, lower_level)
    result["symbol"] = symbol.upper()
    return JsonResponse(result)


def get_candle_detection(request, symbol: str):
    """
    View to detect candle pattern and return signals to frontend.
    """
    try:
        symbol = symbol.strip().upper()

        if not symbol:
            return JsonResponse({"error": "Symbol is missing"}, status=400)

        symbol = validate_symbol(symbol)

        raw_data = request.GET.get("data")

        if raw_data:
            try:
                data_list = json.loads(raw_data)

                if len(data_list) < 5:
                    return JsonResponse({"error": "Not enough data for pattern detection."}, status=400)

                close_prices = np.array([entry["Close"] for entry in data_list if "Close" in entry], dtype=np.float64)
                low_prices = np.array([entry["Low"] for entry in data_list if "Low" in entry], dtype=np.float64)
                high_prices = np.array([entry["High"] for entry in data_list if "High" in entry], dtype=np.float64)
                open_prices = np.array([entry["Open"] for entry in data_list if "Open" in entry], dtype=np.float64)
                dates = np.array([entry["Date"] for entry in data_list if "Date" in entry])

                if np.isnan(close_prices).any() or np.isnan(open_prices).any():
                    return JsonResponse({"error": "Invalid data: missing Close or Open prices."}, status=400)

            except (json.JSONDecodeError, KeyError, TypeError) as e:
                return JsonResponse({"error": f"Invalid data format: {str(e)}"}, status=400)

        else:
            df = dh.get_data_history(symbol=symbol, period="3mo", interval="1d")

            if df is None or df.empty:
                return JsonResponse({"error": "No data found"}, status=404)

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
                detection_result = pattern_func({
                    "Open": open_prices,
                    "High": high_prices,
                    "Low": low_prices,
                    "Close": close_prices
                }, dates)

                if isinstance(detection_result, list) and detection_result:
                    detected_patterns[method_name] = detection_result[-5:]
            except Exception as e:
                detected_patterns[method_name] = f"Error processing pattern: {str(e)}"

        if not detected_patterns:
            return JsonResponse({"symbol": symbol, "patterns_detected": "No patterns found"}, status=200)

        return JsonResponse({"symbol": symbol, "patterns_detected": detected_patterns})

    except Exception as e:
        return JsonResponse({"error": f"Unexpected server error: {str(e)}"}, status=500)


def get_harmonic_patterns(request, symbol: str):
    """
    View to detect harmonic pattern and return signals to frontend.
    """
    try:
        symbol = symbol.strip().upper()

        if not symbol:
            return JsonResponse({"error": "Symbol is missing"}, status=400)

        symbol = validate_symbol(symbol)

        raw_data = request.GET.get("data")

        if raw_data:
            try:
                data_list = json.loads(raw_data)

                if len(data_list) < 5:
                    return JsonResponse({"error": "Not enough data for pattern detection."}, status=400)

            except (json.JSONDecodeError, KeyError, TypeError) as e:
                return JsonResponse({"error": f"Invalid data format: {str(e)}"}, status=400)
        else:
            df = dh.get_data_history(symbol=symbol, period="1mo", interval="1d")

            if df is None or df.empty:
                return JsonResponse({"error": "No data found"}, status=404)

        hp = HarmonicPatterns()

        result = hp.backtest_harmonic_patterns(data=df, err_allowed=0.02, order=5, stop_factor=0.1, future_window=20)

        return JsonResponse({"patterns_detected": result})

    except Exception as e:
        return JsonResponse({"error": f"Unexpected server error: {str(e)}"}, status=500)


def get_inst_holders(request, symbol: str):
    """
    Return the list of major institutional holders
    """
    try:
        symbol = symbol.strip().upper()

        if not symbol:
            return JsonResponse({"error": "Symbol is missing"}, status=400)

        symbol = validate_symbol(symbol)

        df = dh.get_symbol_institutional_holders(symbol)

        if df is None or df.empty:
            return JsonResponse({"error": "No data found"}, status=404)

        df = df.replace({np.nan: None})

        return JsonResponse({"data": df.to_dict(orient="records")})

    except ConnectionError:
        return JsonResponse({"error": "Failed to connect to Yahoo Finance API"}, status=503)

    except Exception as e:
        return JsonResponse({"error": f"Unexpected server error: {str(e)}"}, status=500)


def get_inside_transactions(request, symbol: str):
    """
    Return the list of inside transactions
    """
    try:
        symbol = symbol.strip().upper()

        if not symbol:
            return JsonResponse({"error": "Symbol is missing"}, status=400)

        symbol = validate_symbol(symbol)

        df = dh.get_symbol_inside_transactions(symbol)

        if df is None or df.empty:
            return JsonResponse({"error": "No data found"}, status=404)

        df["StartDate"] = (
            pd.to_datetime(df["StartDate"], utc=True)
            .dt.strftime("%Y-%m-%dT%H:%M:%SZ")  # ISO com 'Z' (UTC)
        )
        df["Shares"] = pd.to_numeric(df["Shares"], errors="coerce")
        df["Value"] = pd.to_numeric(df["Value"],  errors="coerce")
        df = df.replace({np.nan: None})

        return JsonResponse({"data": df.to_dict(orient="records")})

    except ConnectionError:
        return JsonResponse({"error": "Failed to connect to Yahoo Finance API"}, status=503)

    except Exception as e:
        return JsonResponse({"error": f"Unexpected server error: {str(e)}"}, status=500)


def get_recommendations(request, symbol: str):
    """
    Return recommendations about asset
    """
    try:
        symbol = symbol.strip().upper()

        if not symbol:
            return JsonResponse({"error": "Symbol is missing"}, status=400)

        symbol = validate_symbol(symbol)

        df = dh.get_symbol_recommendations(symbol)

        if df is None or df.empty:
            return JsonResponse({"error": "No data found"}, status=404)

        df = df.replace({np.nan: None})

        return JsonResponse({"data": df.to_dict(orient="records")})

    except ConnectionError:
        return JsonResponse({"error": "Failed to connect to Yahoo Finance API"}, status=503)

    except Exception as e:
        return JsonResponse({"error": f"Unexpected server error: {str(e)}"}, status=500)


def get_fundamental_info(request, symbol: str):
    """
    Return fundamnetal information valuation qualitative.
    """
    try:
        symbol = symbol.strip().upper()
        if not symbol:
            return JsonResponse({"error": "Symbol is missing"}, status=400)

        symbol = validate_symbol(symbol)

        fundamental_info = dh.get_symbol_fundamental_info(symbol)

        if not fundamental_info:
            return JsonResponse({"error": "No data found"}, status=404)

        cleaned_data = {}
        for category, data in fundamental_info.items():
            cleaned_data[category] = {
                key: {"value": None if value is np.nan else value}
                for key, value in data.items()
            }

        return JsonResponse(cleaned_data)

    except ConnectionError:
        return JsonResponse({"error": "Failed to connect to Yahoo Finance API"}, status=503)
    except Exception as e:
        return JsonResponse({"error": f"Unexpected server error: {str(e)}"}, status=500)


def get_fundamental_evaluations(request, symbol: str):
    """
    Return only the fundamental evaluation (qualitative data) without nested JSON.
    """
    try:
        symbol = symbol.strip().upper()
        if not symbol:
            return JsonResponse({"error": "Symbol is missing"}, status=400)

        symbol = validate_symbol(symbol)

        fundamental_info = dh.get_symbol_fundamental_info(symbol)

        if not fundamental_info:
            return JsonResponse({"error": "No data found"}, status=404)

        rmf = RiskManagerFundamental()

        evaluations_data = {}

        for category, data in fundamental_info.items():
            evaluation_result = rmf.evaluate_metrics({category: data})

            if isinstance(evaluation_result, dict):
                evaluations_data[category] = evaluation_result
            else:
                evaluations_data[category] = {}

        return JsonResponse({"evaluations": evaluations_data})

    except ConnectionError:
        return JsonResponse({"error": "Failed to connect to Yahoo Finance API"}, status=503)
    except Exception as e:
        return JsonResponse({"error": f"Unexpected server error: {str(e)}"}, status=500)


def get_fundamental_income_download(request, symbol: str):
    """
    Return the income statment
    """
    try:
        symbol = symbol.strip().upper()
        if not symbol:
            return JsonResponse({"error": "Symbol is missing"}, status=400)

        symbol = validate_symbol(symbol)

        income_stmt = dh.get_yahoo_symbol_income(symbol)

        return _df_to_excel_response(income_stmt, f"{symbol}_income_statement")

    except ConnectionError:
        return JsonResponse({"error": "Failed to connect to Yahoo Finance API"}, status=503)
    except Exception as e:
        return JsonResponse({"error": f"Unexpected server error: {str(e)}"}, status=500)


def get_fundamental_balance_sheet_download(request, symbol: str):
    """
    Return the balance sheet
    """
    try:
        symbol = symbol.strip().upper()
        if not symbol:
            return JsonResponse({"error": "Symbol is missing"}, status=400)

        symbol = validate_symbol(symbol)

        balance_sheet = dh.get_yahoo_symbol_balance_sheet(symbol)

        return _df_to_excel_response(balance_sheet, f"{symbol}_balance_sheet")

    except ConnectionError:
        return JsonResponse({"error": "Failed to connect to Yahoo Finance API"}, status=503)
    except Exception as e:
        return JsonResponse({"error": f"Unexpected server error: {str(e)}"}, status=500)


def get_fundamental_cashflow_download(request, symbol: str):
    """
    Return the cashflow
    """
    try:
        symbol = symbol.strip().upper()
        if not symbol:
            return JsonResponse({"error": "Symbol is missing"}, status=400)

        symbol = validate_symbol(symbol)

        cashflow = dh.get_yahoo_symbol_cashflow(symbol)

        return _df_to_excel_response(cashflow, f"{symbol}_cashflow")

    except ConnectionError:
        return JsonResponse({"error": "Failed to connect to Yahoo Finance API"}, status=503)
    except Exception as e:
        return JsonResponse({"error": f"Unexpected server error: {str(e)}"}, status=500)


def get_fundamental_income_quarterly_download(request, symbol: str):
    """
    Return the income statment in quarterly basis
    """
    try:
        symbol = symbol.strip().upper()
        if not symbol:
            return JsonResponse({"error": "Symbol is missing"}, status=400)

        symbol = validate_symbol(symbol)

        income_stmt_quarterly = dh.get_yahoo_symbol_income_quarterly(symbol)

        return _df_to_excel_response(income_stmt_quarterly, f"{symbol}_income_stmt_quarterly")

    except ConnectionError:
        return JsonResponse({"error": "Failed to connect to Yahoo Finance API"}, status=503)
    except Exception as e:
        return JsonResponse({"error": f"Unexpected server error: {str(e)}"}, status=500)


def get_fundamental_balance_sheet_quarterly_download(request, symbol: str):
    """
    Return the balance sheet in quarterly basis
    """
    try:
        symbol = symbol.strip().upper()
        if not symbol:
            return JsonResponse({"error": "Symbol is missing"}, status=400)

        symbol = validate_symbol(symbol)

        balance_sheet_quarterly = dh.get_yahoo_symbol_balance_sheet_quarterly(symbol)

        return _df_to_excel_response(balance_sheet_quarterly, f"{symbol}_balance_sheet_quarterly")

    except ConnectionError:
        return JsonResponse({"error": "Failed to connect to Yahoo Finance API"}, status=503)
    except Exception as e:
        return JsonResponse({"error": f"Unexpected server error: {str(e)}"}, status=500)


def get_fundamental_cashflow_quarterly_download(request, symbol: str):
    """
    Return the cashflow in quarterly basis
    """
    try:
        symbol = symbol.strip().upper()
        if not symbol:
            return JsonResponse({"error": "Symbol is missing"}, status=400)

        symbol = validate_symbol(symbol)

        cashflow_quarterly = dh.get_yahoo_symbol_cashflow_quarterly(symbol)

        return _df_to_excel_response(cashflow_quarterly, f"{symbol}_cashflow_quarterly")

    except ConnectionError:
        return JsonResponse({"error": "Failed to connect to Yahoo Finance API"}, status=503)
    except Exception as e:
        return JsonResponse({"error": f"Unexpected server error: {str(e)}"}, status=500)


def get_bio_info(request, symbol: str):
    """
    Return company information about the company.
    """
    try:
        symbol = symbol.strip().upper()
        if not symbol:
            return JsonResponse({"error": "Symbol is missing"}, status=400)

        symbol = validate_symbol(symbol)

        bio_info = dh.get_symbol_bio_info(symbol)

        if not bio_info:
            return JsonResponse({"error": "No data found"}, status=404)

        bio_info = {k: (None if v == "N/A" else v) for k, v in bio_info.items()}

        return JsonResponse({"data": bio_info})

    except ConnectionError:
        return JsonResponse({"error": "Failed to connect to Yahoo Finance API"}, status=503)

    except Exception as e:
        return JsonResponse({"error": f"Unexpected server error: {str(e)}"}, status=500)


def get_symbol_fundamental_news(request, symbol: str):
    '''
    Return last news from symbol.
    '''
    try:
        symbol = symbol.strip().upper()
        if not symbol:
            return JsonResponse({"error": "Symbol is missing"}, status=400)

        symbol = validate_symbol(symbol)

        news = dh.get_yahoo_symbol_news(symbol)

        if not news:
            return JsonResponse({"error": "No data found"}, status=404)

        return JsonResponse({"data": news})

    except ConnectionError:
        return JsonResponse({"error": "Failed to connect to Yahoo Finance API"}, status=503)

    except Exception as e:
        return JsonResponse({"error": f"Unexpected server error: {str(e)}"}, status=500)


def get_yahoo_symbol_earnings_dates(request, symbol: str):
    '''
    Return the earnings of a symbol over time
    '''
    try:
        symbol = symbol.strip().upper()
        if not symbol:
            return JsonResponse({"error": "Symbol is missing"}, status=400)

        symbol = validate_symbol(symbol)

        df = dh.get_yahoo_symbol_earnings_dates(symbol)

        # sanity check
        if df is None or not isinstance(df, pd.DataFrame) or df.empty:
            return JsonResponse({"data": []}, status=200)

        # ordena por data
        df = df.sort_index()

        # filtra apenas Earnings
        if "Event Type" in df.columns:
            df = df[df["Event Type"] == "Earnings"]

        if df.empty:
            return JsonResponse({"data": []}, status=200)

        # monta lista de dicts
        rows = []
        for idx, row in df.iterrows():
            dt = pd.to_datetime(idx, utc=True, errors="coerce")
            if pd.isna(dt):
                continue

            rows.append({
                "datetime": dt.isoformat(),
                "eps_estimate": float(row["EPS Estimate"]) if pd.notna(row["EPS Estimate"]) else None,
                "reported_eps": float(row["Reported EPS"]) if pd.notna(row["Reported EPS"]) else None,
                "surprise_pct": float(row["Surprise(%)"]) if pd.notna(row["Surprise(%)"]) else None,
                "event_type": str(row["Event Type"]) if pd.notna(row["Event Type"]) else None,
            })

        return JsonResponse({"data": rows}, status=200)

    except ConnectionError:
        return JsonResponse({"error": "Failed to connect to Yahoo Finance API"}, status=503)
    except Exception as e:
        return JsonResponse({"error": f"Unexpected server error: {e}"}, status=500)


# Financial Health Chart
def get_financial_health_chart_info(request, symbol: str):
    """
    Return company information for financial health charts.
    """
    try:
        symbol = symbol.strip().upper()
        if not symbol:
            return JsonResponse({"error": "Symbol is missing"}, status=400)

        symbol = validate_symbol(symbol)

        bio_info = dh.get_symbol_bio_info(symbol)
        bio_fund_info = dh.get_symbol_fundamental_info(symbol)

        if not bio_info:
            return JsonResponse({"error": "No bio data found"}, status=404)

        if not bio_fund_info:
            return JsonResponse({"error": "No fundamental data found"}, status=404)

        company = bio_info.get("LongName") or symbol
        sector = bio_info.get("Sector")
        kpis = bio_fund_info.get("kpis", {})
        metrics = {
            "net_debt_ebitda":       kpis.get("NetDebtEbitda"),
            "interest_coverage":     kpis.get("InterestCoverageEbit"),
            "current_ratio":         kpis.get("CurrentRatio"),
            "quick_ratio":           kpis.get("QuickRatio"),
        }

        thresholds = {
            "nde_neutral":      0.0,
            "nde_strong":       1.0,
            "nde_very_strong":  3.0,
            "ic_weak":          3.0,
            "ic_neutral":       8.0,
        }

        payload = {
            "symbol": symbol,
            "company": company,
            "sector": sector or "Unknown",
            "metrics": metrics,
            "thresholds": thresholds,
            "asof": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "peers": []
        }

        return JsonResponse({"data": payload}, status=200)

    except ConnectionError:
        return JsonResponse({"error": "Failed to connect to Yahoo Finance API"}, status=503)

    except Exception as e:
        return JsonResponse({"error": f"Unexpected server error: {str(e)}"}, status=500)


# Financial Health Chart
def get_profitability_chart_info(request, symbol: str):
    """
    Return company information for profitability charts.
    """
    try:
        symbol = symbol.strip().upper()
        if not symbol:
            return JsonResponse({"error": "Symbol is missing"}, status=400)

        symbol = validate_symbol(symbol)

        bio_info = dh.get_symbol_bio_info(symbol)
        bio_fund_info = dh.get_symbol_fundamental_info_profitability(symbol)

        if not bio_info:
            return JsonResponse({"error": "No bio data found"}, status=404)

        if not bio_fund_info:
            return JsonResponse({"error": "No fundamental data found"}, status=404)

        series = bio_fund_info.get("series")
        if not isinstance(series, dict) or not series:
            return JsonResponse({"error": "No series data found"}, status=404)

        payload = {
            "symbol": symbol,
            "series": bio_fund_info.get("series", {}),
            "series_fy": bio_fund_info.get("series_fy", {}),
            "series_quarter": bio_fund_info.get("series_quarter", {}),
            "asof": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "peers": []
        }

        return JsonResponse({"data": payload}, status=200)

    except ConnectionError:
        return JsonResponse({"error": "Failed to connect to Yahoo Finance API"}, status=503)

    except Exception as e:
        return JsonResponse({"error": f"Unexpected server error: {str(e)}"}, status=500)


# Financial Health Chart
def get_efficiency_chart_info(request, symbol: str):
    """
    Return company information for efficiency (ROIC/WACC/EVA) charts.
    """
    try:
        symbol = (symbol or "").strip().upper()
        if not symbol:
            return JsonResponse({"error": "Symbol is missing"}, status=400)

        symbol = validate_symbol(symbol)

        bio_info = dh.get_symbol_bio_info(symbol)
        cap_eff = dh.get_symbol_fundamental_info_capefficiency(symbol)

        if not bio_info:
            return JsonResponse({"error": "No bio data found"}, status=404)
        if not cap_eff:
            return JsonResponse({"error": "No fundamental data found"}, status=404)

        series_fy = cap_eff.get("series_fy", {})
        if not isinstance(series_fy, dict) or not series_fy.get("labels"):
            return JsonResponse({"error": "No FY series data found"}, status=404)

        payload = {
            "symbol": symbol,
            "series_fy": series_fy,  # {labels, ebit, tax_rate, cap_invested, roic, wacc, eva}
            "asof": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "peers": [],
        }
        return JsonResponse({"data": payload}, status=200)

    except ConnectionError:
        return JsonResponse({"error": "Failed to connect to Yahoo Finance API"}, status=503)
    except Exception as e:
        return JsonResponse({"error": f"Unexpected server error: {str(e)}"}, status=500)
