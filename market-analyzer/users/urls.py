from django.urls import path
from .views import SignUpView, DashboardView
from .watchlist_views import watchlist_add, watchlist_list, watchlist_remove
from .trading_prefs_views import trading_prefs
from .portfolio_views import portfolio_list, portfolio_upsert, portfolio_remove
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('watchlist/', watchlist_list, name='watchlist_list'),
    path('watchlist/add/', watchlist_add, name='watchlist_add'),
    path('watchlist/<str:symbol>/remove/', watchlist_remove, name='watchlist_remove'),
    path('trading-prefs/', trading_prefs, name='trading_prefs'),
    path('portfolio/', portfolio_list, name='portfolio_list'),
    path('portfolio/upsert/', portfolio_upsert, name='portfolio_upsert'),
    path('portfolio/<str:symbol>/remove/', portfolio_remove, name='portfolio_remove'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset_form.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
]
