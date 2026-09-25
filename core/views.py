from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from catalog.models import Equipment, QuoteRequest, Service, ServiceGroup


def home(request):
    context = {
        "featured": Service.objects.filter(featured=True).order_by("order"),
        "groups": ServiceGroup.objects.prefetch_related("services"),
        "equipment": Equipment.objects.all(),
    }
    return render(request, "core/home.html", context)


@require_POST
def quote(request):
    company = request.POST.get("company", "").strip()[:200]
    contact = request.POST.get("contact", "").strip()[:200]
    if not company or not contact:
        return JsonResponse({"ok": False, "error": "Укажите компанию и контакт"}, status=400)
    equipment = Equipment.objects.filter(pk=request.POST.get("equipment") or None).first()
    QuoteRequest.objects.create(
        equipment=equipment, company=company, contact=contact,
        task=request.POST.get("task", "").strip()[:2000],
    )
    # TODO: уведомление на email менеджеру (после настройки почты)
    return JsonResponse({"ok": True})
