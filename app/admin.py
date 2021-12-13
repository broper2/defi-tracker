from django.contrib import admin

from .models import SolanaValidator, SolanaWallet

admin.site.register(SolanaValidator)
admin.site.register(SolanaWallet)
