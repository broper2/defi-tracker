from django.apps import AppConfig as _AppConfig


class AppConfig(_AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
