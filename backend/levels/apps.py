from django.apps import AppConfig


class LevelsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "levels"

    def ready(self):
        from . import signals
