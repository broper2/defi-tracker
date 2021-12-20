from django.contrib import admin

from .models import DefiWallet, DefiValidator

admin.site.register(DefiValidator)
admin.site.register(DefiWallet)
