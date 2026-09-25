from django.contrib import admin
from django.urls import include, path

from config.service_registry import enabled_service_configs

admin.site.site_header = "ecoservices.kz — администрирование"
admin.site.site_title = "ecoservices.kz"


def _service_urlpatterns():
    """Монтирует urls.py каждого включённого сервиса в /services/<service_slug>/."""
    return [
        path(f"services/{config.service_slug}/", include((f"{config.name}.urls", config.name), namespace=config.name))
        for config in enabled_service_configs()
    ]


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    *_service_urlpatterns(),
]
