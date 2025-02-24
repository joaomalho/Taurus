from django.urls import path
from .views import home, stock_page, screener_page, get_yahoo_stock_gainers, get_yahoo_stock_trending, get_yahoo_stock_most_active, get_yahoo_data_history

urlpatterns = [
    path('', home, name='home'),
    path('stock/<str:symbol>/', stock_page, name='stock_page'),
    path('get_yahoo_data_history/', get_yahoo_data_history, name='get_yahoo_data_history'),
    path('screener/', screener_page, name='screener_page'),
    path('screener/get_yahoo_stock_gainers/', get_yahoo_stock_gainers, name='get_yahoo_stock_gainers'),
    path('screener/get_yahoo_stock_trending/', get_yahoo_stock_trending, name='get_yahoo_stock_trending'),
    path('screener/get_yahoo_stock_most_active/', get_yahoo_stock_most_active, name='get_yahoo_stock_most_active'),
]


