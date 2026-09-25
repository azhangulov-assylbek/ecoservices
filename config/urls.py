from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path
from django.views.i18n import JavaScriptCatalog

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
    # Переключатель языка (форма set_language в шапке сайта) — вне языкового префикса,
    # ему активный язык не важен: он только ставит cookie и редиректит по next.
    path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns += i18n_patterns(
    path("", include("core.urls")),
    *_service_urlpatterns(),
    # Каталог переводов для main.js (демо-панель мониторинга) — обязательно внутри
    # i18n_patterns: LocaleMiddleware активирует язык по префиксу URL (/kk/jsi18n/,
    # /en/jsi18n/), иначе для не-префиксного /jsi18n/ он всегда принудительно
    # переключается на LANGUAGE_CODE независимо от куки — main.js получал бы
    # только русский каталог на казахских и английских страницах.
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
    # Русский — язык по умолчанию, для него URL остаётся без префикса /ru/.
    prefix_default_language=False,
)
