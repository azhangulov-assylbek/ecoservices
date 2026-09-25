"""Системные проверки конфигурации сервисов (django check framework).

Регистрируется при старте приложения через core.apps.CoreConfig.ready() —
core всегда установлен, поэтому проверка гарантированно подключается.
"""
from django.apps import apps as django_apps
from django.conf import settings
from django.core.checks import Error, register


@register()
def check_enabled_services(app_configs, **kwargs):
    """Каждый элемент settings.ENABLED_SERVICES должен быть установленным приложением-сервисом."""
    errors = []
    for label in settings.ENABLED_SERVICES:
        try:
            config = django_apps.get_app_config(label)
        except LookupError:
            errors.append(
                Error(
                    f"ENABLED_SERVICES содержит «{label}», но такое приложение не установлено.",
                    hint="Проверьте имя в settings.ENABLED_SERVICES и что оно есть в INSTALLED_APPS.",
                    id="config.E001",
                )
            )
            continue
        if not getattr(config, "service_slug", None):
            errors.append(
                Error(
                    f"Приложение «{label}» указано в ENABLED_SERVICES, но не является сервисом "
                    "(в его AppConfig не задан service_slug).",
                    hint="Задайте service_slug в AppConfig приложения или уберите его из ENABLED_SERVICES.",
                    id="config.E002",
                )
            )
    return errors
