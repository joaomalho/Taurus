from django.urls import path
from .views import home, stock_page, get_stock_data

urlpatterns = [
    path('', home, name='home'),
    path('stock/<str:symbol>/', stock_page, name='stock_page'),
    path('get_stock_data/', get_stock_data, name='get_stock_data'),
]
