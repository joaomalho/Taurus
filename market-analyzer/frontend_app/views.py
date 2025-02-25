from django.shortcuts import render
from django.http import JsonResponse
from backend.datasources.yahoodata import DataHistoryYahoo
from backend.tecnical_analysis.trend_metrics import TrendMetrics  # Ajuste o caminho correto


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
    View que retorna os Top 100 Gainers da Yahoo Finance em formato JSON.
    """
    
    data_history = DataHistoryYahoo() 
    df = data_history.get_yahoo_stocks_top100_gainers()

    if df is None or df.empty:
        return JsonResponse({"error": "No data found"}, status=404)

    # Converte DataFrame para dicionário JSON
    return JsonResponse({"data": df.to_dict(orient="records")})

def get_yahoo_stock_trending(request):
    """
    View que retorna os Top 100 Trending da Yahoo Finance em formato JSON.
    """
    
    data_history = DataHistoryYahoo() 
    df = data_history.get_yahoo_stocks_trending()

    if df is None or df.empty:
        return JsonResponse({"error": "No data found"}, status=404)

    # Converte DataFrame para dicionário JSON
    return JsonResponse({"data": df.to_dict(orient="records")})

def get_yahoo_stock_most_active(request):
    """
    View que retorna os Top 100 Most Active da Yahoo Finance em formato JSON.
    """
    
    data_history = DataHistoryYahoo() 
    df = data_history.get_yahoo_stocks_top100_most_active()

    if df is None or df.empty:
        return JsonResponse({"error": "No data found"}, status=404)

    # Converte DataFrame para dicionário JSON
    return JsonResponse({"data": df.to_dict(orient="records")})


def get_crossover_trend_metrics(request):
    """
    View que calcula o crossover de 3 EMAs e retorna os sinais para o frontend.
    """
    symbol = request.GET.get("symbol", "AAPL")  
    fastperiod = int(request.GET.get("fast", 5))  
    mediumperiod = int(request.GET.get("medium", 10))  
    slowperiod = int(request.GET.get("slow", 20))  

    raw_data = request.GET.get("data")

    if raw_data:
        import json
        data_list = json.loads(raw_data)
        df = pd.DataFrame(data_list)
    else:
        # 🔥 Obtém os dados diretamente do Yahoo (caso não tenham sido carregados no frontend)
        data_history = DataHistoryYahoo()
        df = data_history.get_yahoo_forex_data_history(symbol=symbol, period="1mo", interval="1d")

    if df is None or df.empty:
        return JsonResponse({"error": "No data found"}, status=404)

    # 🔥 Criar um objeto da classe TrendMetrics e calcular crossover
    trend_metrics = TrendMetrics()
    result_df, crossover_info = trend_metrics.get_crossover(df, fastperiod, mediumperiod, slowperiod)

    # 🔥 Retornar JSON
    response_data = {
        "symbol": symbol,
        "fast_period": fastperiod,
        "medium_period": mediumperiod,
        "slow_period": slowperiod,
        "ema1_now": crossover_info.iloc[-1]["ema1_now"],
        "ema2_now": crossover_info.iloc[-1]["ema2_now"],
        "ema3_now": crossover_info.iloc[-1]["ema3_now"],
        "signal": crossover_info.iloc[-1]["signal"]
    }

    return JsonResponse(response_data)
