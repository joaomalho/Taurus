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

def get_stock_data(request):
    symbol = request.GET.get('symbol', '').upper()

    if not symbol:
        return JsonResponse({"error": "No stock symbol provided"}, status=400)

    # Simulação de dados (substitua por API real depois)
    stock_data = {
        "AAPL": {"name": "Apple Inc.", "price": "$180", "change": "+1.5%"},
        "MSFT": {"name": "Microsoft Corp.", "price": "$320", "change": "-0.8%"},
        "GOOGL": {"name": "Alphabet Inc.", "price": "$140", "change": "+2.1%"}
    }

    if symbol in stock_data:
        return JsonResponse({"symbol": symbol, **stock_data[symbol]})
    else:
        return JsonResponse({"error": "Stock not found"}, status=404)


