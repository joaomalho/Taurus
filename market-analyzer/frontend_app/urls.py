from django.urls import path
from .views import (home, stock_page, screener_page, get_stock_gainers, get_stock_trending,
                    get_stock_most_active, get_data_history, get_crossover_trend_metrics, get_adx_trend_metrics,
                    get_sma_trend_metrics, get_rsi_trend_metrics, get_candle_detection, get_inst_holders,
                    get_recommendations, get_fundamental_info
                    )

urlpatterns = [
    ###### MAIN PAGE ######
    path('', home, name='home'),

    ###### PAGE STOCK ######
    path('stock/<str:symbol>/', stock_page, name='stock_page'),

    ###### API: Data for Symbol ######
    path('stock/<str:symbol>/data_history/', get_data_history, name='get_data_history'),
    path('stock/<str:symbol>/crossover_trend/', get_crossover_trend_metrics, name='get_crossover_trend'),
    path('stock/<str:symbol>/adx_trend/', get_adx_trend_metrics, name='get_adx_trend'),
    path('stock/<str:symbol>/bollinger_trend/', get_sma_trend_metrics, name='get_bollinger_trend'),
    path('stock/<str:symbol>/rsi_trend/', get_rsi_trend_metrics, name='get_rsi_trend'),
    path('stock/<str:symbol>/candle_patterns/', get_candle_detection, name='get_candle_patterns'),
    path('stock/<str:symbol>/institutional_holders/', get_inst_holders, name='get_inst_holders'),
    path('stock/<str:symbol>/recommendations/', get_recommendations, name='get_recommendations'),
    path('stock/<str:symbol>/fundamental_info/', get_fundamental_info, name='get_fundamental_info'),

    ###### PAGE SCREENER ######
    path('screener/', screener_page, name='screener_page'),

    ###### API: Screener ######
    path('screener/stock_gainers/', get_stock_gainers, name='get_stock_gainers'),
    path('screener/stock_trending/', get_stock_trending, name='get_stock_trending'),
    path('screener/stock_most_active/', get_stock_most_active, name='get_stock_most_active'),
]

