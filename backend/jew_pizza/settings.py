from collections import OrderedDict
import os
from pathlib import Path
import sys

import environ


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
if os.path.exists("/.env"):
    environ.Env.read_env("/.env")


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
TWILIO_ACCOUNT_SID = env("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = env("TWILIO_AUTH_TOKEN")
AWS_ACCESS_KEY_ID = env("DIGITALOCEAN_SPACES_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("DIGITALOCEAN_SPACES_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("DIGITALOCEAN_SPACES_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = env("DIGITALOCEAN_SPACES_REGION_NAME")

RUN_HUEY = env.bool("__RUN_HUEY", default=False)
GIT_REV = env("GIT_REV", default="unknown")
BUILD_DATE = env("BUILD_DATE", default="unknown")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

ADMINS = [(f"{DOMAIN_NAME} Admin", EMAIL_ADDRESS)]

if DEBUG:
    ALLOWED_HOSTS = ["*"]
else:
    ALLOWED_HOSTS = list({"app", "localhost", "127.0.0.1", DOMAIN_NAME})

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    # 3rd party
    "constance",
    "huey.contrib.djhuey",
    "phonenumber_field",
    "recurrence",
    "s3direct",
    # Local
    "webcore",  # To override the runserver command, place local webcore before staticfiles
    "django.contrib.staticfiles",
    "admin_tools",
    "notifications",
    "radio",
    "shows",
]

if DEBUG:
    INSTALLED_APPS.append("django_extensions")
    SHELL_PLUS_IMPORTS = [
        "from constance import config",
        "from django_redis import get_redis_connection",
        "from jew_pizza.twilio import send_sms, twilio_client",
        "from jew_pizza.utils import reload_radio_container, send_sse_message",
        "from shows.tasks import generate_peaks",
    ]

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

MIGRATION_MODULES = {
    "recurrence": None,
}

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
                "jew_pizza.utils.django_template_context",
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
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        }
    },
    "formatters": {
        "console": {
            "format": "[%(asctime)s] %(levelname)s:%(name)s:%(lineno)s:%(funcName)s: %(message)s",
        },
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "console", "level": "INFO"},
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
            "include_html": True,
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "django.request": {
            "handlers": ["mail_admins", "console"],
            "level": "INFO",
            "propagate": False,
        },
        "huey": {
            "handlers": ["mail_admins", "console"],
            "level": "INFO",
            "propagate": False,
        },
        "jewpizza": {
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

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 10},
            "PARSER_CLASS": "redis.connection.HiredisParser",
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

LANGUAGE_CODE = "en-us"
TIME_ZONE = env("TIMEZONE", default="US/Eastern")
USE_I18N = True
USE_TZ = True
USE_DEPRECATED_PYTZ = True

STATIC_URL = "/static/"
STATIC_ROOT = "/static_root"
MEDIA_URL = "/media/"
MEDIA_ROOT = "/media_root"

# Causes django-recurrence to issue a migration
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

NPM_ROOT_PATH = "/app/frontend"
NPM_STATIC_FILES_PREFIX = "vendor/js"
NPM_FILE_PATTERNS = {
    "alpinejs": ["dist/cdn.min.js"],
    "simpledotcss": ["simple.min.css"],
}

PHONENUMBER_DEFAULT_REGION = "US"

STATICFILES_STORAGE = "jew_pizza.storage.PostProcessCompressionStorage"

AWS_S3_ENDPOINT_URL = f"https://{AWS_S3_REGION_NAME}.digitaloceanspaces.com"
DIGITALOCEAN_SPACES_REWRITE_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.{AWS_S3_REGION_NAME}.digitaloceanspaces.com"
S3DIRECT_DESTINATIONS = {
    "show_asset_url": {
        "key": "shows",
        "auth": lambda u: u.is_staff,
    },
}

CONSTANCE_BACKEND = "constance.backends.redisd.RedisBackend"
CONSTANCE_REDIS_CONNECTION_CLASS = "django_redis.get_redis_connection"
CONSTANCE_SUPERUSER_ONLY = False
CONSTANCE_IGNORE_ADMIN_VERSION_CHECK = True
CONSTANCE_ADDITIONAL_FIELDS = {
    "char": ("django.forms.CharField",),
    "phone": ("phonenumber_field.formfields.PhoneNumberField",),
    "url": ("django.forms.URLField",),
    "uuid_optional": ("django.forms.UUIDField", {"required": False}),
    "icecast_protocol": (
        "django.forms.ChoiceField",
        {"choices": (("http", "http (insecure)"), ("https", "https (secure)"))},
    ),
    "positive_int": ("django.forms.IntegerField", {"min_value": 1}),
}
CONSTANCE_CONFIG = {
    "ENABLE_JEWIPPY": (True, "Enable jewippy at bottom of page"),
    "ENABLE_PLAYER": (False, "Enable audio player"),
    "ENABLE_TEST_NOTIFICATIONS": (False, "Enable test notifications on home page (for superuser only)"),
    "HIDDEN_IMG_MODE": (False, "Enable hidden image mode (for development in public, to not look so awkward)"),
    "TWILIO_FROM_NUMBER": ("+14164390000", "Twilio from number for texts/calls", "phone"),
    "LOGS_URL": (
        "http://localhost:8888/" if DEBUG else "https://logs.jew.pizza/",
        "URL for logs container, linked in admin",
        "url",
    ),
    "UMAMI_URL": ("http://localhost:3000/" if DEBUG else "https://umami.jew.pizza/", "URL for umami analytics", "url"),
    "UMAMI_SCRIPT_URL": (
        "http://localhost:3000/" if DEBUG else "https://umami.jew.pizza/script.js",
        "URL for umami.js script",
        "url",
    ),
    "UMAMI_WEBSITE_ID": ("", "Website ID in umami", "uuid_optional"),
    "SSE_URL": (
        "http://localhost:8001/" if DEBUG else "https://sse.jew.pizza/",
        "URL for server-sent events endpoint",
        "url",
    ),
    "ICECAST_URL": (
        "http://localhost:8080/" if DEBUG else "https://radio.jew.pizza/",
        "Public URL for Icecast server",
        "url",
    ),
    "ICECAST_HOSTNAME": ("icecast" if DEBUG else "host.docker.internal", "Hostname for Icecast server", "char"),
    "ICECAST_PORT": (8000, "Port for Icecast server", "positive_int"),
    "ICECAST_USERNAME": ("source", "Username for Icecast server", "char"),
    "ICECAST_PASSWORD": ("hackme", "Password for Icecast server", "char"),
    "ICECAST_PROTOCOL": ("http", "Protocol for Icecast server", "icecast_protocol"),
    "AUTO_DEPLOY": (True, "Automatically deploy from Github Actions when code is pushed to main branch"),
}

CONSTANCE_CONFIG_FIELDSETS = OrderedDict(
    (
        ("Development Options", ("ENABLE_JEWIPPY", "ENABLE_PLAYER", "ENABLE_TEST_NOTIFICATIONS", "HIDDEN_IMG_MODE")),
        ("Telephony", ("TWILIO_FROM_NUMBER",)),
        ("Umami Tracking Tag", ("UMAMI_WEBSITE_ID", "UMAMI_URL", "UMAMI_SCRIPT_URL")),
        (
            "Icecast",
            (
                "ICECAST_URL",
                "ICECAST_HOSTNAME",
                "ICECAST_PORT",
                "ICECAST_USERNAME",
                "ICECAST_PASSWORD",
                "ICECAST_PROTOCOL",
            ),
        ),
        ("Miscellaneous", ("LOGS_URL", "SSE_URL", "AUTO_DEPLOY")),
    )
)
