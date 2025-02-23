from django.urls import path
from .views import home, stock_page, get_stock_data, screener_page, get_yahoo_gainers

urlpatterns = [
    path('', home, name='home'),
    path('stock/<str:symbol>/', stock_page, name='stock_page'),
    path('get_stock_data/', get_stock_data, name='get_stock_data'),
    path('screener/', screener_page, name='screener_page'),
    path('screener/get_yahoo_gainers/', get_yahoo_gainers, name='get_yahoo_gainers'),
]


