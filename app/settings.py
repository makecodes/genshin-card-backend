import os
from pathlib import Path

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

BASE_DIR = Path(__file__).resolve().parent.parent

SCOPE = os.getenv("SCOPE", "production")

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN", ""),
    integrations=[
        DjangoIntegration(),
    ],
    send_default_pii=True,
    environment=SCOPE,
)

SECRET_KEY = os.getenv("SECRET_KEY", "changeme")

DEBUG = os.getenv("DEBUG", "0") in ["1", "true"]

ALLOWED_HOSTS = ["*"]

APPEND_SLASH = False

INSTALLED_APPS = [
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_api_key",
    "django_extensions",
    "django_json_widget",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "sorl.thumbnail",
    "storages",
    "core",
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

AUTH_USER_MODEL = "core.User"

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["./templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "debug": DEBUG,
        },
    }
]

WSGI_APPLICATION = "app.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DB_NAME", "genshin"),
        "USER": os.getenv("DB_USER", "root"),
        "PASSWORD": os.getenv("DB_PASSWORD", "genshin"),
        "HOST": os.getenv("DB_HOST", "mysql"),
        "PORT": os.getenv("DB_PORT", "3306"),
        "OPTIONS": {"charset": "utf8mb4"},
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = []

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 50,
}

DEFAULT_FILE_STORAGE = os.getenv(
    "DEFAULT_FILE_STORAGE", "django.core.files.storage.FileSystemStorage"
)


STATIC_URL = os.getenv("MINIO_STATIC_URL", "/static/")
MEDIA_URL = os.getenv("MINIO_MEDIA_URL", "/media/")

STATIC_ROOT = BASE_DIR / "static"
MEDIA_ROOT = BASE_DIR / "media"

MINIO_STORAGE_ENDPOINT = os.getenv("MINIO_STORAGE_ENDPOINT", "static.makecodes.dev")
MINIO_STORAGE_ACCESS_KEY = os.getenv("MINIO_STORAGE_ACCESS_KEY", "minio")
MINIO_STORAGE_SECRET_KEY = os.getenv("MINIO_STORAGE_SECRET_KEY", "minio123")
MINIO_STORAGE_USE_HTTPS = int(os.getenv("MINIO_STORAGE_USE_HTTPS", "1")) in [1]
MINIO_STORAGE_MEDIA_BUCKET_NAME = os.getenv(
    "MINIO_STORAGE_MEDIA_BUCKET_NAME", "mcmedia"
)
MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET = int(
    os.getenv("MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET", "1")
) in [1]
MINIO_STORAGE_STATIC_BUCKET_NAME = os.getenv(
    "MINIO_STORAGE_STATIC_BUCKET_NAME", "mcstatic"
)
MINIO_STORAGE_AUTO_CREATE_STATIC_BUCKET = int(
    os.getenv("MINIO_STORAGE_AUTO_CREATE_STATIC_BUCKET", "1")
) in [1]
MINIO_REGION = os.getenv("MINIO_REGION", "sa-east-1")


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            # exact format is not important, this is the minimum information
            "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
    },
    "loggers": {
        "": {
            "level": "INFO",
            "handlers": ["console"],
        },
    },
}


CSRF_TRUSTED_ORIGINS = [
    "https://qagenshin.makecodes.dev",
    "https://genshin.makecodes.dev",
    "https://devgenshin.makecodes.dev",
]
