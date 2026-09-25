from django.test import TestCase, override_settings
from django.utils import translation

from catalog.models import Equipment, Service, ServiceGroup


class LocalizedFieldTests(TestCase):
    """Значение на активном языке с откатом на русский, если перевод не заполнен."""

    def setUp(self):
        self.service = Service.objects.get(slug="ndt-check")

    def test_russian_is_default(self):
        with translation.override("ru"):
            self.assertEqual(self.service.display_name, self.service.name)
            self.assertEqual(self.service.display_description, self.service.description)

    def test_kazakh_and_english_translations_are_used(self):
        with translation.override("kk"):
            self.assertEqual(self.service.display_name, self.service.name_kk)
        with translation.override("en"):
            self.assertEqual(self.service.display_name, self.service.name_en)

    def test_missing_translation_falls_back_to_russian(self):
        group = ServiceGroup.objects.create(name="Тестовая группа")  # name_kk/name_en пустые
        with translation.override("kk"):
            self.assertEqual(group.display_name, "Тестовая группа")
        with translation.override("en"):
            self.assertEqual(group.display_name, "Тестовая группа")

    def test_equipment_display_parameters(self):
        equipment = Equipment.objects.get(name="Выбросы")
        with translation.override("en"):
            self.assertEqual(equipment.display_parameters, equipment.parameters_en)
            self.assertTrue(equipment.display_parameters)

    @override_settings(LANGUAGE_CODE="ru")
    def test_unsupported_language_code_falls_back_to_russian(self):
        # get_language() может вернуть код, не входящий в TRANSLATABLE_LANGUAGES
        # (например, диалект без перевода) — тогда используем русский без ошибок.
        with translation.override("fr"):
            self.assertEqual(self.service.display_name, self.service.name)
