from django.shortcuts import get_object_or_404, render

from catalog.models import Service

from .apps import EsgP5Config


def index(request):
    """Стартовая страница сервиса. Название, описание и статус — из catalog.Service."""
    service = get_object_or_404(Service, slug=EsgP5Config.service_slug)
    return render(request, "esg_p5/index.html", {"service": service})
