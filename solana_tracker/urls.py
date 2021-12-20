from django.contrib import admin
from django.urls import include, path
from app.views import create_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create_user', create_user, name='create_user'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('<str:network>', include('app.urls')),
]