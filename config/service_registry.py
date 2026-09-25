"""Реестр сервисов-приложений платформы.

Composition root (`config/`) — единственное место в проекте, которое обращается
к сервисам по имени (наряду с settings.INSTALLED_APPS и config/urls.py). Весь
остальной код (`core`, `catalog`, сами сервисы) работает с сервисами только
через этот модуль, а не через прямой import сервисного приложения. Подробнее
о правилах — в docs/architecture.md.
"""
from django.apps import apps as django_apps
from django.conf import settings
from django.urls import NoReverseMatch, reverse


def enabled_service_configs():
    """AppConfig подключённых и включённых сервисов, в порядке settings.ENABLED_SERVICES.

    Приложение попадает в список, только если оно установлено (INSTALLED_APPS)
    и его AppConfig определяет атрибут service_slug.
    """
    configs = []
    for label in settings.ENABLED_SERVICES:
        try:
            config = django_apps.get_app_config(label)
        except LookupError:
            continue
        if getattr(config, "service_slug", None):
            configs.append(config)
    return configs


def service_url_map():
    """Словарь {catalog.Service.slug: адрес стартовой страницы} для включённых сервисов.

    Строится через reverse(), поэтому адрес автоматически получает языковой префикс
    (/kk/services/..., /en/services/...) для текущего активного языка запроса.
    """
    urls = {}
    for config in enabled_service_configs():
        try:
            urls[config.service_slug] = reverse(f"{config.name}:index")
        except NoReverseMatch:
            continue
    return urls
