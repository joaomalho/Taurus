import json
import numpy as np
from django.shortcuts import render
from django.http import JsonResponse
from backend.datasources.yahoodata import DataHistoryYahoo
from backend.tecnical_analysis.trend_metrics import TrendMetrics
from backend.tecnical_analysis.candles_patterns import CandlesPatterns


############################# Pages #############################
def home(request):
    return render(request, 'index.html')

############################# Screener Page #############################

def screener_page(request):
    return render(request, 'screener.html')

############################# Stock Pages #############################

def stock_page(request, symbol):
    return render(request, 'stock.html', {"symbol": symbol})


def get_yahoo_data_history(request):
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
        ticker = request.GET.get("symbol", "EURUSD=X")
        per = request.GET.get("period", "1mo")
        interval_time = request.GET.get("interval", "1d")

        try:
            data_history = DataHistoryYahoo()  
            df = data_history.get_yahoo_data_history(symbol=ticker, period=per, interval=interval_time)
            
            if df is None or df.empty:
                return JsonResponse({"error": "No data found"}, status=404)

            return JsonResponse({"data": df.to_dict(orient="records")})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        

def get_yahoo_stock_gainers(request):
    """
    View to pass Top 100 Gainers JSON.
    """
    
    data_history = DataHistoryYahoo() 
    df = data_history.get_yahoo_stocks_top100_gainers()

    if df is None or df.empty:
        return JsonResponse({"error": "No data found"}, status=404)

    # Converte DataFrame para dicionário JSON
    return JsonResponse({"data": df.to_dict(orient="records")})

def get_yahoo_stock_trending(request):
    """
    View to pass Top 100 Trending JSON.
    """
    
    data_history = DataHistoryYahoo() 
    df = data_history.get_yahoo_stocks_trending()

    if df is None or df.empty:
        return JsonResponse({"error": "No data found"}, status=404)

    # Converte DataFrame para dicionário JSON
    return JsonResponse({"data": df.to_dict(orient="records")})

def get_yahoo_stock_most_active(request):
    """
    View to pass Top 100 Most Active JSON.
    """
    
    data_history = DataHistoryYahoo() 
    df = data_history.get_yahoo_stocks_top100_most_active()

    if df is None or df.empty:
        return JsonResponse({"error": "No data found"}, status=404)

    # Converte DataFrame para dicionário JSON
    return JsonResponse({"data": df.to_dict(orient="records")})


def get_crossover_trend_metrics(request):
    """
    View to calculate crossover of 3 EMAs and return signals to frontend.
    """
    symbol = request.GET.get("symbol", "").strip().upper()

    if not symbol:
        return JsonResponse({"error": "Symbol is missing"}, status=400)

    fastperiod = int(request.GET.get("fast", 5))
    mediumperiod = int(request.GET.get("medium", 10))
    slowperiod = int(request.GET.get("slow", 20))

    raw_data = request.GET.get("data")

    if raw_data:
        try:
            data_list = json.loads(raw_data)
            close_prices = np.array([entry["Close"] for entry in data_list if "Close" in entry], dtype=np.float64)
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            return JsonResponse({"error": f"Invalid data format: {str(e)}"}, status=400)
    else:
        data_history = DataHistoryYahoo()
        df = data_history.get_yahoo_data_history(symbol=symbol, period="1mo", interval="1d")

        if df is None or df.empty:
            return JsonResponse({"error": "No data found"}, status=404)

        close_prices = df["Close"].to_numpy(dtype=np.float64) 

    tm = TrendMetrics()
    crossover_result = tm.get_crossover(close_prices, symbol, fastperiod, mediumperiod, slowperiod)

    return JsonResponse(crossover_result)


def get_adx_trend_metrics(request):
    """
    View to calculate ADX and return signals to frontend.
    """
    symbol = request.GET.get("symbol", "").strip().upper()

    if not symbol:
        return JsonResponse({"error": "Symbol is missing"}, status=400)

    length = int(request.GET.get("length", 5))

    raw_data = request.GET.get("data")

    if raw_data:
        try:
            data_list = json.loads(raw_data)
            close_prices = np.array([entry["Close"] for entry in data_list if "Close" in entry], dtype=np.float64)
            high_prices = np.array([entry["High"] for entry in data_list if "High" in entry], dtype=np.float64)
            low_prices = np.array([entry["Low"] for entry in data_list if "Low" in entry], dtype=np.float64)
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            return JsonResponse({"error": f"Invalid data format: {str(e)}"}, status=400)
    else:
        data_history = DataHistoryYahoo()
        df = data_history.get_yahoo_data_history(symbol=symbol, period="1mo", interval="1d")

        if df is None or df.empty:
            return JsonResponse({"error": "No data found"}, status=404)

        close_prices = df["Close"].to_numpy(dtype=np.float64) 
        high_prices = df["High"].to_numpy(dtype=np.float64) 
        low_prices = df["Low"].to_numpy(dtype=np.float64) 

    tm = TrendMetrics()
    adx_result = tm.get_adx(high_prices, low_prices, close_prices, symbol, length)

    return JsonResponse(adx_result)


def get_sma_trend_metrics(request):
    """
    View to calculate Bollinger and return signals to frontend.
    """
    symbol = request.GET.get("symbol", "").strip().upper()

    if not symbol:
        return JsonResponse({"error": "Symbol is missing"}, status=400)

    length = int(request.GET.get("length", 5))
    std_dev = int(request.GET.get("std_dev", 5))

    raw_data = request.GET.get("data")

    if raw_data:
        try:
            data_list = json.loads(raw_data)
            close_prices = np.array([entry["Close"] for entry in data_list if "Close" in entry], dtype=np.float64)
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            return JsonResponse({"error": f"Invalid data format: {str(e)}"}, status=400)
    else:
        data_history = DataHistoryYahoo()
        df = data_history.get_yahoo_data_history(symbol=symbol, period="1mo", interval="1d")

        if df is None or df.empty:
            return JsonResponse({"error": "No data found"}, status=404)

        close_prices = df["Close"].to_numpy(dtype=np.float64) 

    tm = TrendMetrics()
    sma_bands_result = tm.get_sma_bands(symbol, close_prices, length, std_dev)

    return JsonResponse(sma_bands_result)


def get_rsi_trend_metrics(request):
    """
    View to calculate RSI and return signals to frontend.
    """
    symbol = request.GET.get("symbol", "").strip().upper()

    if not symbol:
        return JsonResponse({"error": "Symbol is missing"}, status=400)

    length = int(request.GET.get("length", 5))
    upper_level = int(request.GET.get("upper_level", 5))
    lower_level = int(request.GET.get("lower_level", 5))

    raw_data = request.GET.get("data")

    if raw_data:
        try:
            data_list = json.loads(raw_data)
            close_prices = np.array([entry["Close"] for entry in data_list if "Close" in entry], dtype=np.float64)
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            return JsonResponse({"error": f"Invalid data format: {str(e)}"}, status=400)
    else:
        data_history = DataHistoryYahoo()
        df = data_history.get_yahoo_data_history(symbol=symbol, period="1mo", interval="1d")

        if df is None or df.empty:
            return JsonResponse({"error": "No data found"}, status=404)

        close_prices = df["Close"].to_numpy(dtype=np.float64) 

    tm = TrendMetrics()
    rsi_result = tm.get_rsi(symbol, close_prices, length, upper_level, lower_level)

    return JsonResponse(rsi_result)


def get_candle_detection(request):
    """
    View to detect candle pattern and return signals to frontend.
    """
    symbol = request.GET.get("symbol", "").strip().upper()

    if not symbol:
        return JsonResponse({"error": "Symbol is missing"}, status=400)

    raw_data = request.GET.get("data")

    if raw_data:
        try:
            data_list = json.loads(raw_data)
            close_prices = np.array([entry["Close"] for entry in data_list if "Close" in entry], dtype=np.float64)
            low_prices = np.array([entry["Low"] for entry in data_list if "Low" in entry], dtype=np.float64)
            high_prices = np.array([entry["High"] for entry in data_list if "High" in entry], dtype=np.float64)
            open_prices = np.array([entry["Open"] for entry in data_list if "Open" in entry], dtype=np.float64)
            dates = np.array([entry["Date"] for entry in data_list if "Date" in entry])
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            return JsonResponse({"error": f"Invalid data format: {str(e)}"}, status=400)
    else:
        data_history = DataHistoryYahoo()
        df = data_history.get_yahoo_data_history(symbol=symbol, period="1mo", interval="1d")

        if df is None or df.empty:
            return JsonResponse({"error": "No data found"}, status=404)

        close_prices = df["Close"].to_numpy(dtype=np.float64) 
        low_prices = df["Low"].to_numpy(dtype=np.float64) 
        high_prices = df["High"].to_numpy(dtype=np.float64) 
        open_prices = df["Open"].to_numpy(dtype=np.float64) 

    cp = CandlesPatterns()

    detected_patterns = {}

    for method_name in dir(cp):
        if not method_name.startswith("_") and callable(getattr(cp, method_name)):  # Evita métodos internos
            try:
                pattern_func = getattr(cp, method_name)
                detection_result = pattern_func({
                    "Open": open_prices, "High": high_prices, "Low": low_prices, "Close": close_prices
                })

                # Filtra sinais diferentes de zero (padrões detectados)
                detected_indices = np.nonzero(detection_result)[0]
                if detected_indices.size > 0:
                    detected_patterns[method_name] = {
                        dates[i]: int(detection_result[i]) for i in detected_indices
                    }
            except Exception as e:
                detected_patterns[method_name] = f"Error processing pattern: {str(e)}"

    return JsonResponse({"symbol": symbol, "patterns_detected": detected_patterns})