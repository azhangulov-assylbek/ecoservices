from django.test import TestCase
from django.urls import reverse

from catalog.models import Equipment, QuoteRequest, Service


class HomeTests(TestCase):
    def test_home_renders_catalog_from_db(self):
        r = self.client.get(reverse("core:home"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "ecoservices")
        # данные из начальной миграции
        self.assertGreaterEqual(Service.objects.count(), 10)
        self.assertContains(r, "ESG-отчёт по стандарту P5")
        self.assertContains(r, "Проверка объекта по НДТ")

    def test_quote_saved(self):
        eq = Equipment.objects.first()
        r = self.client.post(reverse("core:quote"), {"equipment": eq.pk, "company": "ТОО Тест", "contact": "a@b.kz", "task": "котельная"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(QuoteRequest.objects.get().equipment, eq)

    def test_quote_requires_fields(self):
        r = self.client.post(reverse("core:quote"), {"company": ""})
        self.assertEqual(r.status_code, 400)
