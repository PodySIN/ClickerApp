from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

DEBUG = os.environ.get("DEBUG", True)

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "debug_toolbar",
    "django_celery_beat",
    "unfold",
    "unfold.contrib.filters",
    "import_export",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_spectacular",
    "corsheaders",
    "users",
    "tasks",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
    }
}

REDIS_CACHE_HOST = os.getenv("REDIS_CACHE_HOST", "redis-cache")
REDIS_CELERY_HOST = os.getenv("REDIS_CELERY_HOST", "redis-celery")
REDIS_CACHE_PORT = os.getenv("REDIS_CACHE_PORT", "6379")
REDIS_CELERY_PORT = os.getenv("REDIS_CELERY_PORT", "6378")
REDIS_CACHE_DB = os.getenv("REDIS_CACHE_DB", "0")
REDIS_CELERY_DB = os.getenv("REDIS_CELERY_DB", "0")

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_CACHE_HOST}:{REDIS_CACHE_PORT}/{REDIS_CACHE_DB}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

CELERY_BROKER_URL = f"redis://{REDIS_CELERY_HOST}:{REDIS_CELERY_PORT}/{REDIS_CELERY_DB}"
CELERY_RESULT_BACKEND = f"redis://{REDIS_CELERY_HOST}:{REDIS_CELERY_PORT}/{REDIS_CELERY_DB}"
CELERY_TIME_ZONE = "Europe/Moscow"
CELERY_ENABLE_UTC = True
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "ru-ru"  # или 'ru'
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_L10N = True


CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "generated-user-id",
    "access-control-allow-origin",
    "X-Telegram-InitData",
    "x-telegram-initdata",
    "Access-Control-Allow-Origin",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:80",
]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATIC_URL = "/static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Clicker App API",
    "DESCRIPTION": "Clicker App API",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

UNFOLD = {
    "SITE_TITLE": "Админка тапалки",
    "SITE_HEADER": "Администрирование",
    "SITE_URL": "/",
    "THEME": "dark",
    "COLORS": {
        "primary": {
            "50": "250 245 255",
            "100": "243 232 255",
            "200": "233 213 255",
            "300": "216 180 254",
            "400": "192 132 252",
            "500": "168 85 247",
            "600": "147 51 234",
            "700": "126 34 206",
            "800": "107 33 168",
            "900": "88 28 135",
        },
    },
}
