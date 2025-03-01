from django.urls import path
from .views import home, stock_page, screener_page, get_yahoo_stock_gainers, get_yahoo_stock_trending, get_yahoo_stock_most_active, get_yahoo_data_history, get_crossover_trend_metrics, get_adx_trend_metrics, get_sma_trend_metrics, get_rsi_trend_metrics, get_candle_detection

urlpatterns = [
    path('', home, name='home'),
    path('stock/<str:symbol>/', stock_page, name='stock_page'),
    path('get_yahoo_data_history/', get_yahoo_data_history, name='get_yahoo_data_history'),
    path('screener/', screener_page, name='screener_page'),
    path('screener/get_yahoo_stock_gainers/', get_yahoo_stock_gainers, name='get_yahoo_stock_gainers'),
    path('screener/get_yahoo_stock_trending/', get_yahoo_stock_trending, name='get_yahoo_stock_trending'),
    path('screener/get_yahoo_stock_most_active/', get_yahoo_stock_most_active, name='get_yahoo_stock_most_active'),
    path('get_crossover_trend/', get_crossover_trend_metrics, name='get_crossover_trend'),
    path('get_adx_trend/', get_adx_trend_metrics, name='get_adx_trend'),
    path('get_bollinger_trend/', get_sma_trend_metrics, name='get_bollinger_trend'),
    path('get_rsi_trend/', get_rsi_trend_metrics, name='get_rsi_trend'),
    path('get_candle_patterns/', get_candle_detection, name='get_candle_patterns'),
]

