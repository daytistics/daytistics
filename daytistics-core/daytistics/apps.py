from django.apps import AppConfig

class DaytisticsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'daytistics'

    def ready(self):
        import activities.signals