from django.apps import AppConfig

class DocumentosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'documentos'

    def ready(self):
        from documentos.setup_grupos import setup_grupos
        setup_grupos()
