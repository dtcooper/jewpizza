import os
from pathlib import Path
import sys

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
if os.path.exists("/.env"):
    env.read_env("/.env")


SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG", default=False)
DOMAIN_NAME = env("DOMAIN_NAME", default="jew.pizza")

# For testing gunicorn only.
SERVE_ASSETS_FROM_DJANGO = env("SERVE_ASSETS_FROM_DJANGO", default=False)

EMAIL_HOST = env("EMAIL_HOST")
EMAIL_HOST_USER = env("EMAIL_USERNAME")
EMAIL_HOST_PASSWORD = env("EMAIL_PASSWORD")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=(EMAIL_PORT == 587))
DEFAULT_FROM_EMAIL = env("EMAIL_FROM_ADDRESS")
UMAMI_SCRIPT_URL = env("UMAMI_SCRIPT_URL", default=None)
UMAMI_WEBSITE_ID = env("UMAMI_WEBSITE_ID", default=None)
TWILIO_ACCOUNT_SID = env("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = env("TWILIO_AUTH_TOKEN")
TWILIO_FROM_NUMBER = env("TWILIO_FROM_NUMBER")

ICECAST_URL = env("ICECAST_URL")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

if DEBUG:
    ALLOWED_HOSTS = ["*"]
else:
    ALLOWED_HOSTS = list({"app", "localhost", "127.0.0.1", DOMAIN_NAME})

INSTALLED_APPS = [
    "django_light",  # Disable admin
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    # To override the runserver command, place local webcore before staticfiles
    "webcore",
    "django.contrib.staticfiles",
    # 3rd party
    "phonenumber_field",
    "recurrence",
    # Local
    "notifications",
    "shows",
]

if DEBUG:
    INSTALLED_APPS.append("django_extensions")

MIDDLEWARE = ["django.middleware.security.SecurityMiddleware"]
if not DEBUG and SERVE_ASSETS_FROM_DJANGO:
    MIDDLEWARE.append("whitenoise.middleware.WhiteNoiseMiddleware")
MIDDLEWARE.extend(
    [
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "webcore.middleware.JSONResponseMiddleware",
    ]
)
if DEBUG and len(sys.argv) >= 2 and sys.argv[1] == "runserver":
    MIDDLEWARE.append("webcore.middleware.TailwindFunctioningRunserverMiddleware")

ROOT_URLCONF = "jew_pizza.urls"

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
    {
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "autoescape": lambda filename: any(filename.endswith(ext) for ext in (".xml", ".html")),
            "keep_trailing_newline": True,
            "environment": "jew_pizza.jinja2.environment",
            "extensions": [
                "jinja2.ext.do",
                "jinja2.ext.loopcontrols",
            ],
            "context_processors": [
                "jew_pizza.jinja2.nav_links",
            ],
        },
    },
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "format": "[%(asctime)s] %(levelname)s:%(name)s:%(lineno)s:%(funcName)s: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}

WSGI_APPLICATION = "jew_pizza.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "db",
        "PORT": 5432,
    }
}

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

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 10},
        },
        "KEY_PREFIX": "cache",
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

EMAIL_TIMEOUT = 10

LANGUAGE_CODE = "en-us"
TIME_ZONE = env("TIMEZONE", default="US/Eastern")
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = "/static_root"
MEDIA_URL = "/media/"
MEDIA_ROOT = "/media_root"

# Causes django-recurrence to issue a migration
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

NPM_ROOT_PATH = "/app/frontend"
NPM_STATIC_FILES_PREFIX = "js/vendor"
NPM_FILE_PATTERNS = {
    "alpinejs": ["dist/cdn.min.js"],
    "@alpinejs/persist": ["dist/cdn.min.js"],
    "moment": ["min/moment.min.js"],
    "moment-timezone": ["builds/moment-timezone-with-data-1970-2030.min.js"],
    "navigo": ["lib/navigo.min.js"],
}

PHONENUMBER_DEFAULT_REGION = "US"

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "npm.finders.NpmFinder",
]
