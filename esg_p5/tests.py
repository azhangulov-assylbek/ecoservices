from django.test import TestCase
from django.urls import reverse

from catalog.models import Service


class EsgP5IndexTests(TestCase):
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
