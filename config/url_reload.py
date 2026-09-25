"""Тестовая утилита: пересборка config.urls после изменения ENABLED_SERVICES.

urlpatterns в config/urls.py собираются один раз при импорте модуля, поэтому
обычный override_settings(ENABLED_SERVICES=...) не меняет реально смонтированные
маршруты. enabled_services() форсирует пересборку urlconf на время блока —
используется только в тестах.
"""
import importlib
from contextlib import contextmanager

from django.test import override_settings
from django.urls import clear_url_caches

import config.urls as _urls_module


@contextmanager
def enabled_services(*labels):
    """Временно задаёт ENABLED_SERVICES и пересобирает urlconf на время блока."""
    try:
        with override_settings(ENABLED_SERVICES=list(labels)):
            clear_url_caches()
            importlib.reload(_urls_module)
            yield
    finally:
        # Возвращаем urlconf в соответствие с настоящим settings.ENABLED_SERVICES.
        clear_url_caches()
        importlib.reload(_urls_module)
