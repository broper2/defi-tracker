from django.urls import path

from . import views

urlpatterns = [
    path('', views.defi_index, name='defi_index'),
    path('validators/delete', views.delete_validator, name='delete_validator'),
    path('validators', views.validators, name='validators'),
    path('wallets', views.wallets, name='wallets'),
]
