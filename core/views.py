from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from catalog.models import Equipment, QuoteRequest, Service, ServiceGroup
from config.service_registry import service_url_map


def home(request):
    urls = service_url_map()
    featured = list(Service.objects.filter(featured=True).order_by("order"))
    groups = list(ServiceGroup.objects.prefetch_related("services"))
    # Адрес реального сервиса, если он подключён и включён (settings.ENABLED_SERVICES).
    # Статус сервиса в базе (Service.status) не решает, вести ли на страницу сервиса —
    # он только определяет подпись бейджа.
    for s in featured:
        s.service_url = urls.get(s.slug)
    for group in groups:
        for s in group.services.all():
            s.service_url = urls.get(s.slug)
    context = {
        "featured": featured,
        "groups": groups,
        "equipment": Equipment.objects.all(),
    }
    return render(request, "core/home.html", context)


@require_POST
def quote(request):
    company = request.POST.get("company", "").strip()[:200]
    contact = request.POST.get("contact", "").strip()[:200]
    if not company or not contact:
        return JsonResponse({"ok": False, "error": _("Укажите компанию и контакт")}, status=400)
    equipment = Equipment.objects.filter(pk=request.POST.get("equipment") or None).first()
    QuoteRequest.objects.create(
        equipment=equipment, company=company, contact=contact,
        task=request.POST.get("task", "").strip()[:2000],
    )
    # TODO: уведомление на email менеджеру (после настройки почты)
    return JsonResponse({"ok": True})
