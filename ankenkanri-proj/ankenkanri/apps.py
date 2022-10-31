from django.apps import AppConfig


class AnkenkanriConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ankenkanri'

#     def ready(self):
#         from .ap_scheduler import start
#         start()
