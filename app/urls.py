from django.urls import path

from . import views

urlpatterns = [
    path('/', views.index, name='solana_index'),
    path('/validators', views.validators, name='validators'),
    path('/wallets', views.wallets, name='wallets'),
]