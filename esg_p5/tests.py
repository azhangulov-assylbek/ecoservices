from django.test import TestCase
from django.urls import reverse
from django.utils import translation

from catalog.models import Service


class EsgP5IndexTests(TestCase):
    def tearDown(self):
        # См. пояснение в core.tests.HomeLanguageTests.tearDown: запрос к /kk/... активирует
        # язык на весь поток теста, и это нужно сбросить, иначе он «утечёт» в другие тесты.
        translation.deactivate_all()

    def test_page_renders_service_from_catalog(self):
        service = Service.objects.get(slug="esg-p5")
        r = self.client.get(reverse("esg_p5:index"))
        self.assertEqual(r.status_code, 200)
        self.assertTemplateUsed(r, "esg_p5/index.html")
        self.assertContains(r, service.name)
        self.assertContains(r, service.description)
        self.assertContains(r, "Бета")

    def test_mounted_at_services_slug_url(self):
        r = self.client.get("/services/esg-p5/")
        self.assertEqual(r.status_code, 200)

    def test_page_is_translated_for_other_languages(self):
        service = Service.objects.get(slug="esg-p5")
        r = self.client.get("/kk/services/esg-p5/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, service.name_kk)
        self.assertContains(r, "Бета, қолданып көруге болады")
