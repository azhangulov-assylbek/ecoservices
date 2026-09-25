from django.apps import AppConfig


class NdtCheckConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ndt_check'
    service_slug = 'ndt-check'
