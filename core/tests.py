from django.test import TestCase
from django.urls import reverse

from catalog.models import Equipment, QuoteRequest, Service
from config.url_reload import enabled_services


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

    def test_open_button_links_to_enabled_service(self):
        r = self.client.get(reverse("core:home"))
        self.assertContains(r, '/services/ndt-check/')
        self.assertContains(r, '/services/esg-p5/')

    def test_open_button_falls_back_to_notify_when_service_disabled(self):
        # ndt-check в базе имеет статус "beta" — но пока сервис не подключён
        # (не входит в ENABLED_SERVICES), кнопка должна вести не на страницу
        # сервиса, а предлагать подписаться на запуск. Статус влияет только
        # на подпись бейджа, не на то, есть ли рабочая ссылка.
        service = Service.objects.get(slug="ndt-check")
        self.assertEqual(service.status, Service.Status.BETA)
        with enabled_services("esg_p5"):
            r = self.client.get(reverse("core:home"))
        self.assertNotContains(r, '/services/ndt-check/')
        self.assertContains(r, "Сообщить о запуске")
        self.assertContains(r, '/services/esg-p5/')
