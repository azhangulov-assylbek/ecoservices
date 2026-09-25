from django.test import TestCase
from django.urls import reverse

from catalog.models import Service


class NdtCheckIndexTests(TestCase):
    def test_page_renders_service_from_catalog(self):
        service = Service.objects.get(slug="ndt-check")
        r = self.client.get(reverse("ndt_check:index"))
        self.assertEqual(r.status_code, 200)
        self.assertTemplateUsed(r, "ndt_check/index.html")
        self.assertContains(r, service.name)
        self.assertContains(r, service.description)
        self.assertContains(r, "Бета")

    def test_mounted_at_services_slug_url(self):
        r = self.client.get("/services/ndt-check/")
        self.assertEqual(r.status_code, 200)
