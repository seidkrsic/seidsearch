from django.apps import AppConfig


class UserAppConfig(AppConfig):
    name = 'user_app'
    default_auto_field = 'django.db.models.BigAutoField' 
    def ready(self): 
        import user_app.signals
