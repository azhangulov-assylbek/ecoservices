import json

from django.test import TestCase
from django.urls import reverse
from django.utils import translation

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


class HomeLanguageTests(TestCase):
    """Русский — без префикса в URL, остальные языки — через /kk/ и /en/."""

    def tearDown(self):
        # Запрос к /kk/ или /en/ активирует язык в LocaleMiddleware на текущий поток;
        # Django не сбрасывает это между тестами (в отличие от реального сервера, где
        # каждый следующий запрос активирует язык заново). Сбрасываем явно, иначе более
        # ранний тест этого класса «просачивается» в другие тесты, использующие reverse()
        # вне запроса (например, ServiceRegistryTests или HomeTests).
        translation.deactivate_all()

    def test_default_russian_has_no_url_prefix(self):
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Войти")

    def test_kazakh_prefixed_home_page_is_translated(self):
        r = self.client.get("/kk/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Кіру")  # «Войти»
        self.assertContains(r, "Ашу")  # «Открыть»

    def test_english_prefixed_home_page_is_translated(self):
        r = self.client.get("/en/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Log in")
        self.assertContains(r, "Open service")

    def test_catalog_content_is_translated_per_language(self):
        r_ru = self.client.get("/")
        r_en = self.client.get("/en/")
        self.assertContains(r_ru, "Проверка объекта по НДТ")
        self.assertContains(r_en, "BAT compliance check")

    def test_set_language_switches_and_redirects_to_prefixed_url(self):
        r = self.client.post(reverse("set_language"), {"language": "kk", "next": "/"}, follow=True)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.redirect_chain[-1][0], "/kk/")
        self.assertContains(r, "Кіру")

    def test_javascript_catalog_reflects_page_language(self):
        # javascript-catalog смонтирован внутри i18n_patterns: язык определяется
        # префиксом URL (как его сгенерирует {% url %} на странице соответствующего
        # языка), а не активным языком запроса — LocaleMiddleware форсирует
        # LANGUAGE_CODE для непрефиксных путей (см. комментарий в config/urls.py).
        # Django сериализует каталог как JS-объект с \uXXXX-экранированием не-ASCII —
        # ищем ту же escape-форму, а не буквальную кириллицу.
        escaped = json.dumps("Хабарлаймыз")[1:-1]
        r = self.client.get("/kk/jsi18n/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, escaped)
        r_ru = self.client.get("/jsi18n/")
        self.assertEqual(r_ru.status_code, 200)
        self.assertNotContains(r_ru, escaped)

    def test_home_page_loads_language_matching_js_catalog(self):
        r = self.client.get("/kk/")
        self.assertContains(r, 'src="/kk/jsi18n/"')
