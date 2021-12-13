from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('validators', views.validators, name='validators'),
    path('wallets', views.wallets, name='wallets'),
    path('create_user', views.create_user, name='create_user'),
]