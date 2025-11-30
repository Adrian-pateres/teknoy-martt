from django.apps import AppConfig


class TeknoyMartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'teknoymart'
    
    # Only add ready() if you need signals
    # def ready(self):
    #     import teknoymart.signals
