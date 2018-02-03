"""
Canonical settings for the project.
"""
import os
import sys

from celery.schedules import crontab
from decouple import config
from dj_database_url import parse as db_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS_DIR = os.path.join(BASE_DIR, "apps")
sys.path.insert(0, APPS_DIR)

DEBUG = config("DEBUG", cast=bool)
SECRET_KEY = config("SECRET_KEY")
SITE_URL = config("SITE_URL")
ENV = config("ENV")
ENV_COLOR = config("ENV_COLOR", default="#808080")
ALLOWED_HOSTS = ["*"]  # TODO: Change to allowed domains

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "django_extensions",

    "tickers",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "coinsy.urls"
WSGI_APPLICATION = "coinsy.wsgi.application"

# Database
DATABASES = {"default": config("DATABASE_URL", cast=db_url)}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
DATABASES["default"]["CONN_MAX_AGE"] = 60

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Auth
# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME":
        "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files
STATIC_DEV = os.path.join(BASE_DIR, "static_dev")
STATICFILES_DIRS = (STATIC_DEV, )
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATIC_URL = "/static/"


# celery
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_BROKER_URL = config("REDIS_URL")
CELERY_REDIS_MAX_CONNECTIONS = 20
CELERY_RESULT_BACKEND = config("REDIS_URL")
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_RESULT_EXPIRES = 60 * 60  # seconds
CELERY_TASK_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
CELERY_WORKER_CONCURRENCY = 4

CELERY_BEAT_SCHEDULER = "redbeat.RedBeatScheduler"
CELERY_BEAT_SCHEDULE = {
    "celery.backend_cleanup": {
        "task": "celery.backend_cleanup",
        "schedule": crontab(minute="0", hour="*"),  # every hour
        "options": {
            "expires": 30 * 60  # seconds
        }
    },
}

# sentry/raven
RAVEN_DSN = None
