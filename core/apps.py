from django.apps import AppConfig
from django.contrib import admin


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from .models import Popup
        from .admin import PopupAdmin
        admin.site.register(Popup, PopupAdmin)
