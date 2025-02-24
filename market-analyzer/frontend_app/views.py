from django.shortcuts import render
from django.http import JsonResponse
from backend.datasources.yahoodata import DataHistoryYahoo

############################# Pages #############################
def home(request):
    return render(request, 'index.html')

############################# Screener Page #############################

def screener_page(request):
    return render(request, 'screener.html')

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