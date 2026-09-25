from django.shortcuts import get_object_or_404, render

from catalog.models import Service

from .apps import NdtCheckConfig


def index(request):
    """Стартовая страница сервиса. Название, описание и статус — из catalog.Service."""
    service = get_object_or_404(Service, slug=NdtCheckConfig.service_slug)
    return render(request, "ndt_check/index.html", {"service": service})
