import json
import numpy as np
from django.shortcuts import render
from django.http import JsonResponse, Http404
from django.core.validators import RegexValidator
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

############################# Security Validations #############################
def validate_symbol(symbol):
    """
    Valida se o símbolo é uma string alfanumérica com no máximo 10 caracteres.
    """
    validator = RegexValidator(regex=r'^[A-Z0-9]{1,10}$', message="Invalid symbol format.")
    try:
        validator(symbol)
        return symbol
    except Exception:
        raise Http404("Invalid stock symbol.")

def get_yahoo_data_history(request, symbol):
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
                data_history = DataHistoryYahoo()  
                df = data_history.get_yahoo_data_history(symbol=symbol, period=per, interval=interval_time)
                
                if df is None or df.empty:
                    return JsonResponse({"error": "No data found"}, status=404)

                return JsonResponse({"data": df.to_dict(orient="records")})

            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
        except Exception as e:
            return JsonResponse({"error": f"Unexpected server error: {str(e)}"}, status=500)

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
    try:
        data_history = DataHistoryYahoo() 
        df = data_history.get_yahoo_stocks_trending()

        if df is None or df.empty:
            return JsonResponse({"error": "No data found"}, status=404)

        # Converte DataFrame para dicionário JSON
        return JsonResponse({"data": df.to_dict(orient="records")})

    except ConnectionError:
        return JsonResponse({"error": "Failed to connect to Provider API"}, status=503)

    except Exception as e:
        return JsonResponse({"error": f"Unexpected server error: {str(e)}"}, status=500)

def get_yahoo_stock_most_active(request):
    """
    View to pass Top 100 Most Active JSON.
    """
    try:
        data_history = DataHistoryYahoo() 
        df = data_history.get_yahoo_stocks_top100_most_active()

        if df is None or df.empty:
            return JsonResponse({"error": "No data found"}, status=404)

        # Converte DataFrame para dicionário JSON
        return JsonResponse({"data": df.to_dict(orient="records")})

    except ConnectionError:
        return JsonResponse({"error": "Failed to connect to Provider API"}, status=503)

    except Exception as e:
        return JsonResponse({"error": f"Unexpected server error: {str(e)}"}, status=500)


def get_crossover_trend_metrics(request, symbol):
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
            data_history = DataHistoryYahoo()
            df = data_history.get_yahoo_data_history(symbol=symbol, period="1mo", interval="1d")

            if df is None or df.empty:
                return JsonResponse({"error": "No data found"}, status=404)

            close_prices = df["Close"].to_numpy(dtype=np.float64) 

        tm = TrendMetrics()
        crossover_result = tm.get_crossover(close_prices, symbol, fastperiod, mediumperiod, slowperiod)

        return JsonResponse(crossover_result)
    
    except Exception as e:
        return JsonResponse({"error": f"Unexpected server error: {str(e)}"}, status=500)

def get_adx_trend_metrics(request, symbol):
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

    except Exception as e:
        return JsonResponse({"error": f"Unexpected server error: {str(e)}"}, status=500)

def get_sma_trend_metrics(request, symbol):
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
            data_history = DataHistoryYahoo()
            df = data_history.get_yahoo_data_history(symbol=symbol, period="1mo", interval="1d")

            if df is None or df.empty:
                return JsonResponse({"error": "No data found"}, status=404)

            close_prices = df["Close"].to_numpy(dtype=np.float64) 

        tm = TrendMetrics()
        sma_bands_result = tm.get_sma_bands(symbol, close_prices, length, std_dev)

        return JsonResponse(sma_bands_result)
    
    except Exception as e:
        return JsonResponse({"error": f"Unexpected server error: {str(e)}"}, status=500)
    
def get_rsi_trend_metrics(request, symbol):
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
            data_history = DataHistoryYahoo()
            df = data_history.get_yahoo_data_history(symbol=symbol, period="1mo", interval="1d")

            if df is None or df.empty:
                return JsonResponse({"error": "No data found"}, status=404)

            close_prices = df["Close"].to_numpy(dtype=np.float64) 

        tm = TrendMetrics()
        rsi_result = tm.get_rsi(symbol, close_prices, length, upper_level, lower_level)

        return JsonResponse(rsi_result)

    except Exception as e:
        return JsonResponse({"error": f"Unexpected server error: {str(e)}"}, status=500)
 

def get_candle_detection(request, symbol):
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
                
                # Validando se há pelo menos 5 candles nos dados
                if len(data_list) < 5:
                    return JsonResponse({"error": "Not enough data for pattern detection."}, status=400)
                

                close_prices = np.array([entry["Close"] for entry in data_list if "Close" in entry], dtype=np.float64)
                low_prices = np.array([entry["Low"] for entry in data_list if "Low" in entry], dtype=np.float64)
                high_prices = np.array([entry["High"] for entry in data_list if "High" in entry], dtype=np.float64)
                open_prices = np.array([entry["Open"] for entry in data_list if "Open" in entry], dtype=np.float64)
                dates = np.array([entry["Date"] for entry in data_list if "Date" in entry])

                # Checando se há valores NaN nos dados
                if np.isnan(close_prices).any() or np.isnan(open_prices).any():
                    return JsonResponse({"error": "Invalid data: missing Close or Open prices."}, status=400)

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
                    detected_patterns[method_name] = detection_result[-5:]  # Pega os últimos 5 resultados
            except Exception as e:
                detected_patterns[method_name] = f"Error processing pattern: {str(e)}"

        if not detected_patterns:
            return JsonResponse({"symbol": symbol, "patterns_detected": "No patterns found"}, status=200)

        return JsonResponse({"symbol": symbol, "patterns_detected": detected_patterns})

    except Exception as e:
        return JsonResponse({"error": f"Unexpected server error: {str(e)}"}, status=500)

def get_yahoo_inst_holders(request, symbol):
    """
    Return the list of major institutional holders
    """
    try:
        symbol = symbol.strip().upper()

        if not symbol:
            return JsonResponse({"error": "Symbol is missing"}, status=400)

        symbol = validate_symbol(symbol)

        data_history = DataHistoryYahoo()  
        df = data_history.get_yahoo_symbol_institutional_holders(symbol)
        
        if df is None or df.empty:
            return JsonResponse({"error": "No data found"}, status=404)

        df = df.replace({np.nan: None})

        return JsonResponse({"data": df.to_dict(orient="records")})

    except ConnectionError:
        return JsonResponse({"error": "Failed to connect to Yahoo Finance API"}, status=503)

    except Exception as e:
        return JsonResponse({"error": f"Unexpected server error: {str(e)}"}, status=500)
