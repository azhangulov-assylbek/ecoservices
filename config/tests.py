"""Тесты выбора подключения к базе данных."""
from django.test import SimpleTestCase

from config.settings import BASE_DIR, build_database_config


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
