from django.core.cache import cache
from django.core.validators import RegexValidator
from django.db import models
from django.utils.safestring import mark_safe

from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

from .constants import CACHE_KEY_PREFIX_CONTENT_BLOCK


class ContentBlock(models.Model):
    CACHE_EXPIRE_TIME = 60 * 60  # 1 hour

    name = models.CharField(
        "block name",
        max_length=255,
        unique=True,
        help_text='In slug format, ie "placeholder.content"',
        validators=[
            RegexValidator(r"^[a-zA-Z0-9_\.\-]+$", message="Must contain only numbers, letters, periods or hyphens")
        ],
    )
    content = MarkdownxField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.set(
            f"{CACHE_KEY_PREFIX_CONTENT_BLOCK}{self.name}", markdownify(self.content), timeout=self.CACHE_EXPIRE_TIME
        )

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        cache.delete(f"{CACHE_KEY_PREFIX_CONTENT_BLOCK}{self.name}")

    @classmethod
    def render_content_block(cls, name):
        cache_key = f"{CACHE_KEY_PREFIX_CONTENT_BLOCK}{name}"

        content = cache.get(cache_key)
        if not content:
            block, _ = cls.objects.get_or_create(name=name, defaults={"content": name})
            content = markdownify(block.content)
            cache.set(cache_key, content, timeout=cls.CACHE_EXPIRE_TIME)

        return mark_safe(content)
