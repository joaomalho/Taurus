from django.urls import path
from .views import (home, stock_page, screener_page, get_stock_gainers, get_stock_trending,
                    get_stock_most_active, get_data_history, get_crossover_trend_metrics, get_adx_trend_metrics,
                    get_bollinger_bands_metrics, get_rsi_trend_metrics, get_candle_detection, get_inst_holders,
                    get_recommendations, get_fundamental_info, get_bio_info, get_fundamental_evaluations,
                    get_harmonic_patterns, get_crossover_trend_metrics_draw, get_bollinger_bands_metrics_draw,
                    get_inside_transactions, get_rsi_trend_metrics_draw, get_fundamental_income_download, 
                    get_fundamental_cashflow_download, get_fundamental_balance_sheet_download,
                    get_fundamental_income_quarterly_download, get_fundamental_cashflow_quarterly_download,
                    get_fundamental_balance_sheet_quarterly_download
                    )

urlpatterns = [
    # ------ MAIN PAGE ------
    path('', home, name='home'),

    # ------ PAGE STOCK ------
    path('stock/<str:symbol>/', stock_page, name='stock_page'),

    # ------ API: Data for Symbol ------
    path('stock/<str:symbol>/bio_info/', get_bio_info, name='get_bio_info'),
    path('stock/<str:symbol>/data_history/', get_data_history, name='get_data_history'),
    path('stock/<str:symbol>/crossover_trend/', get_crossover_trend_metrics, name='get_crossover_trend'),
    path('stock/<str:symbol>/adx_trend/', get_adx_trend_metrics, name='get_adx_trend'),
    path('stock/<str:symbol>/bollinger_trend/', get_bollinger_bands_metrics, name='get_bollinger_trend'),
    path('stock/<str:symbol>/rsi_trend/', get_rsi_trend_metrics, name='get_rsi_trend'),
    path('stock/<str:symbol>/candle_patterns/', get_candle_detection, name='get_candle_patterns'),
    path('stock/<str:symbol>/harmonic_patterns/', get_harmonic_patterns, name='get_harmonic_patterns'),
    path('stock/<str:symbol>/fundamental_info/', get_fundamental_info, name='get_fundamental_info'),
    path('stock/<str:symbol>/fundamental_evaluations/', get_fundamental_evaluations, name='fundamental_evaluations'),
    path('stock/<str:symbol>/institutional_holders/', get_inst_holders, name='get_inst_holders'),
    path('stock/<str:symbol>/inside_transactions/', get_inside_transactions, name='get_inside_transactions'),
    path('stock/<str:symbol>/recommendations/', get_recommendations, name='get_recommendations'),

    # ------ Candlestick Chart Draw ------
    path("stock/<str:symbol>/crossover_draw/", get_crossover_trend_metrics_draw, name='get_crossover_trend_metrics_draw'),
    path("stock/<str:symbol>/bollinger_draw/", get_bollinger_bands_metrics_draw, name='get_bollinger_bands_metrics_draw'),
    path("stock/<str:symbol>/rsi_draw/", get_rsi_trend_metrics_draw, name='get_rsi_trend_metrics_draw'),

    # ------ PAGE SCREENER ------
    path('screener/', screener_page, name='screener_page'),

    # ------ API: Screener ------
    path('screener/stock_gainers/', get_stock_gainers, name='get_stock_gainers'),
    path('screener/stock_trending/', get_stock_trending, name='get_stock_trending'),
    path('screener/stock_most_active/', get_stock_most_active, name='get_stock_most_active'),

    # ------ Downloads ------
    path('stock/<str:symbol>/income_download/', get_fundamental_income_download, name='get_fundamental_income_download'),
    path('stock/<str:symbol>/cashflow_download/', get_fundamental_cashflow_download, name='get_fundamental_cashflow_download'),
    path('stock/<str:symbol>/balance_sheet_download/', get_fundamental_balance_sheet_download, name='get_fundamental_balance_sheet_download'),
    path('stock/<str:symbol>/income_quarterly_download/', get_fundamental_income_quarterly_download, name='get_fundamental_income_quarterly_download'),
    path('stock/<str:symbol>/cashflow_quarterly_download/', get_fundamental_cashflow_quarterly_download, name='get_fundamental_cashflow_quarterly_download'),
    path('stock/<str:symbol>/balance_sheet_quarterly_download/', get_fundamental_balance_sheet_quarterly_download, name='get_fundamental_balance_sheet_quarterly_download'),
]
