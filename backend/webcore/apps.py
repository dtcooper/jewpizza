from django.apps import AppConfig
from django.core.cache import cache

from jew_pizza.j2_env import STATIC_MD5_CACHE_KEY_PREFIX


class WebcoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "webcore"
    verbose_name = 'Application Core'

    def ready(self):
        # Clear static asset MD5 cache
        cache.delete_pattern(f"{STATIC_MD5_CACHE_KEY_PREFIX}*")
