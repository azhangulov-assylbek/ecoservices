"""Тесты выбора подключения к базе данных и реестра сервисов."""
from django.test import SimpleTestCase, TestCase, override_settings

from config.checks import check_enabled_services
from config.service_registry import enabled_service_configs, service_url_map
from config.settings import BASE_DIR, build_database_config
from config.url_reload import enabled_services


class BuildDatabaseConfigTests(SimpleTestCase):
    def test_database_url_has_priority(self):
        config = build_database_config(
            {
                "DATABASE_URL": "postgres://u:p@example.org:5432/base",
                "POSTGRES_DB": "ignored",
                "POSTGRES_USER": "ignored",
            }
        )
        self.assertEqual(config["ENGINE"], "django.db.backends.postgresql")
        self.assertEqual(config["NAME"], "base")
        self.assertEqual(config["USER"], "u")
        self.assertEqual(config["HOST"], "example.org")

    def test_postgres_variables_build_connection_to_host_db(self):
        config = build_database_config(
            {
                "POSTGRES_DB": "ecoservices",
                "POSTGRES_USER": "ecoservices",
                "POSTGRES_PASSWORD": "секрет",
            }
        )
        self.assertEqual(
            config,
            {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": "ecoservices",
                "USER": "ecoservices",
                "PASSWORD": "секрет",
                "HOST": "db",
                "PORT": "5432",
                "CONN_MAX_AGE": 600,
            },
        )

    def test_postgres_host_and_port_can_be_overridden(self):
        config = build_database_config(
            {
                "POSTGRES_DB": "ecoservices",
                "POSTGRES_USER": "ecoservices",
                "POSTGRES_HOST": "10.0.0.5",
                "POSTGRES_PORT": "6432",
            }
        )
        self.assertEqual(config["HOST"], "10.0.0.5")
        self.assertEqual(config["PORT"], "6432")

    def test_sqlite_without_variables(self):
        config = build_database_config({})
        self.assertEqual(config["ENGINE"], "django.db.backends.sqlite3")
        self.assertEqual(config["NAME"], str(BASE_DIR / "db.sqlite3"))

    def test_incomplete_postgres_variables_fall_back_to_sqlite(self):
        config = build_database_config({"POSTGRES_DB": "ecoservices"})
        self.assertEqual(config["ENGINE"], "django.db.backends.sqlite3")


class ServiceRegistryTests(SimpleTestCase):
    def test_default_enabled_services_have_matching_slugs(self):
        slugs = {config.service_slug for config in enabled_service_configs()}
        self.assertEqual(slugs, {"ndt-check", "esg-p5"})

    def test_service_url_map_points_to_services_prefix(self):
        urls = service_url_map()
        self.assertEqual(urls["ndt-check"], "/services/ndt-check/")
        self.assertEqual(urls["esg-p5"], "/services/esg-p5/")

    @override_settings(ENABLED_SERVICES=["ndt_check"])
    def test_disabled_service_is_not_in_registry(self):
        self.assertEqual(service_url_map(), {"ndt-check": "/services/ndt-check/"})

    @override_settings(ENABLED_SERVICES=["not_an_app", "catalog"])
    def test_unknown_or_non_service_apps_are_ignored(self):
        # catalog установлен, но не сервис (нет service_slug); not_an_app не установлен вовсе.
        self.assertEqual(enabled_service_configs(), [])


class CheckEnabledServicesTests(SimpleTestCase):
    def test_default_configuration_has_no_errors(self):
        self.assertEqual(check_enabled_services(None), [])

    @override_settings(ENABLED_SERVICES=["not_an_app"])
    def test_error_when_app_is_not_installed(self):
        errors = check_enabled_services(None)
        self.assertEqual([e.id for e in errors], ["config.E001"])

    @override_settings(ENABLED_SERVICES=["catalog"])
    def test_error_when_app_has_no_service_slug(self):
        errors = check_enabled_services(None)
        self.assertEqual([e.id for e in errors], ["config.E002"])


class ServiceUrlMountingTests(TestCase):
    """Проверяет, что ENABLED_SERVICES реально управляет монтированием маршрутов."""

    def test_only_enabled_service_is_reachable(self):
        with enabled_services("esg_p5"):
            self.assertEqual(self.client.get("/services/esg-p5/").status_code, 200)
            self.assertEqual(self.client.get("/services/ndt-check/").status_code, 404)
        # После выхода из блока монтирование возвращается к настоящему ENABLED_SERVICES.
        self.assertEqual(self.client.get("/services/ndt-check/").status_code, 200)
