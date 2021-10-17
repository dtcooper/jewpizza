from collections import OrderedDict
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

EMAIL_ADDRESS = env("EMAIL_ADDRESS")
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_HOST_USER = env("EMAIL_USERNAME")
EMAIL_HOST_PASSWORD = env("EMAIL_PASSWORD")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=(EMAIL_PORT == 587))
DEFAULT_FROM_EMAIL = SERVER_EMAIL = env("EMAIL_FROM_ADDRESS")
UMAMI_SCRIPT_URL = env("UMAMI_SCRIPT_URL", default=None)
UMAMI_WEBSITE_ID = env("UMAMI_WEBSITE_ID", default=None)
TWILIO_ACCOUNT_SID = env("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = env("TWILIO_AUTH_TOKEN")
TWILIO_FROM_NUMBER = env("TWILIO_FROM_NUMBER")
LOAD_SHOWS_DEV_EXPORT_URL = env("LOAD_SHOWS_DEV_EXPORT_URL", default="https://jew.pizza/shows/dev-export/")
SUBSTACK_NAME = env("SUBSTACK_NAME", default="jewpizza")
TWITTER_NAME = env("TWITTER_NAME", default="dtcooper")
INSTAGRAM_NAME = env("INSTAGRAM_NAME", default="dtcooper")
FACEBOOK_NAME = env("FACEBOOK_NAME", default="dtcooper")
RUN_HUEY = env("__RUN_HUEY", default=False)

ICECAST_URL = env("ICECAST_URL")
LOGS_URL = env("LOGS_URL")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

ADMINS = [(f"{DOMAIN_NAME} Admin", EMAIL_ADDRESS)]

if DEBUG:
    ALLOWED_HOSTS = ["*"]
else:
    ALLOWED_HOSTS = list({"app", "localhost", "127.0.0.1", DOMAIN_NAME})

INSTALLED_APPS = [
    "django_light",  # Disable admin dark mode
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    # 3rd party
    "constance",
    "durationwidget",
    "djhuey_email",
    "huey.contrib.djhuey",
    "phonenumber_field",
    "recurrence",
    # Local
    "webcore",  # To override the runserver command, place local webcore before staticfiles
    "django.contrib.staticfiles",
    "admin_tools",
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
        "DIRS": [BASE_DIR / "jew_pizza" / "templates"],  # For admin override
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
            "environment": "jew_pizza.jinja2.create_environment",
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
        "console": {"class": "logging.StreamHandler", "formatter": "console", "level": "INFO"},
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "jewpizza": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}

if not DEBUG:
    LOGGING["handlers"]["mail_admins"] = {
        "level": "ERROR",
        "class": "django.utils.log.AdminEmailHandler",
        "include_html": True,
    }
    email_admin_logger = {
        "handlers": ["mail_admins", "console"],
        "level": "INFO",
        "propagate": False,
    }

    LOGGING["loggers"].update({"django.request": email_admin_logger, "huey": email_admin_logger})

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

HUEY = {
    "connection": {"host": "redis"},
    "expire_time": 60 * 60,
    "huey_class": "huey.PriorityRedisExpireHuey",
    "immediate": False,
    "name": "jewpizza",
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

if not RUN_HUEY:  # Don't run emails async using huey
    EMAIL_BACKEND = "djhuey_email.backends.HueyEmailBackend"

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
NPM_STATIC_FILES_PREFIX = "vendor/js"
NPM_FILE_PATTERNS = {
    "@alpinejs/persist": ["dist/cdn.min.js"],
    "alpinejs": ["dist/cdn.min.js"],
    "moment-timezone": ["builds/moment-timezone-with-data-1970-2030.min.js"],
    "moment": ["min/moment.min.js"],
    "navigo": ["lib/navigo.min.js"],
    "simpledotcss": ["simple.min.css"],
}

PHONENUMBER_DEFAULT_REGION = "US"

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "npm.finders.NpmFinder",
]

CONSTANCE_BACKEND = "constance.backends.redisd.RedisBackend"
CONSTANCE_REDIS_CONNECTION_CLASS = "django_redis.get_redis_connection"
CONSTANCE_SUPERUSER_ONLY = False
CONSTANCE_CONFIG = OrderedDict(
    (
        ("ENABLE_JEWIPPY", (True, "Enable jewippy at bottom of page")),
        ("ENABLE_PLAYER", (False, "Enable audio player")),
        ("ENABLE_TEST_NOTIFICATIONS", (False, "Enable test notifications on home page for superuser only.")),
        ("HIDDEN_IMG_MODE", (False, "Enable hidden image mode (for development in public, to not look so awkward)")),
    )
)
