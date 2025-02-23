from django.shortcuts import render
from django.http import JsonResponse

def home(request):
    return render(request, 'index.html')

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
