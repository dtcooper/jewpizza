from django.apps import AppConfig
from django.core.cache import cache

from .constants import CACHE_KEY_PREFIX_STATIC_ASSET_MD5SUM


class WebcoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "webcore"
    verbose_name = "Application Core"

    def ready(self):
        # Clear static asset MD5 cache
        cache.delete_pattern(f"{CACHE_KEY_PREFIX_STATIC_ASSET_MD5SUM}*")
