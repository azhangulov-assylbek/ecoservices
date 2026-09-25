"""Настройки ecoservices.kz. Все секреты и параметры окружения берутся из переменных окружения (.env)."""
import os
import sys
from pathlib import Path

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name, default=False):
    return os.environ.get(name, str(default)).lower() in ("1", "true", "yes", "on")


SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-insecure-change-me")
DEBUG = env_bool("DJANGO_DEBUG", True)
ALLOWED_HOSTS = [h.strip() for h in os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if h.strip()]
CSRF_TRUSTED_ORIGINS = [o.strip() for o in os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",") if o.strip()]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
    "catalog",
    "ndt",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.site",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# База данных: сначала DATABASE_URL, затем PostgreSQL из POSTGRES_*,
# иначе SQLite для быстрого локального запуска без Docker.
_CONN_MAX_AGE = 600


def build_database_config(env=None):
    """Подключение к базе: DATABASE_URL -> POSTGRES_* -> SQLite."""
    env = os.environ if env is None else env
    url = env.get("DATABASE_URL", "").strip()
    if url:
        return dj_database_url.parse(url, conn_max_age=_CONN_MAX_AGE)
    name = env.get("POSTGRES_DB", "").strip()
    user = env.get("POSTGRES_USER", "").strip()
    if name and user:
        return {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": name,
            "USER": user,
            "PASSWORD": env.get("POSTGRES_PASSWORD", ""),
            # В docker compose база доступна по имени сервиса db.
            "HOST": env.get("POSTGRES_HOST", "db"),
            "PORT": env.get("POSTGRES_PORT", "5432"),
            "CONN_MAX_AGE": _CONN_MAX_AGE,
        }
    return {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": str(BASE_DIR / "db.sqlite3"),
    }


DATABASES = {"default": build_database_config()}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "ru"
TIME_ZONE = "Asia/Almaty"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}
if "test" in sys.argv:  # тестам не нужен собранный манифест статики
    STORAGES["staticfiles"] = {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"}
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Контакты компании для шаблонов
SITE_CONTACTS = {
    "company": "ТОО «ЭКОМЕКЕН»",
    "company_url": "https://www.ecomeken.kz/ru/",
    "email": os.environ.get("SITE_EMAIL", "info@ecomeken.kz"),
    "phone": os.environ.get("SITE_PHONE", "+7 708 511 5249"),
}

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = env_bool("DJANGO_SSL_REDIRECT", True)
    SECURE_HSTS_SECONDS = 3600
    SECURE_CONTENT_TYPE_NOSNIFF = True
