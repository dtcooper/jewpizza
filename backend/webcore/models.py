from django.core.cache import cache
from django.db import models

from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from django.core.validators import RegexValidator
from django.utils.safestring import mark_safe


class ContentBlock(models.Model):
    CACHE_KEY_PREFIX = "content_block::"
    CACHE_EXPIRE_TIME = 12 * 60 * 60  # 12 hours

    name = models.CharField("block name", max_length=255, unique=True, help_text='In slug format, ie "placeholder.content"',
    validators=[RegexValidator(r'^[a-zA-Z0-9_\.\-]+$', message='Must contain only numbers, letters, periods or hyphens')])
    content = MarkdownxField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.set(f"{self.CACHE_KEY_PREFIX}{self.name}", markdownify(self.content), timeout=self.CACHE_EXPIRE_TIME)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        cache.delete(f"{self.CACHE_KEY_PREFIX}{self.name}")

    @classmethod
    def render_content_block(cls, name):
        cache_key = f"{cls.CACHE_KEY_PREFIX}{name}"

        content = cache.get(cache_key)
        if not content:
            block, _ = cls.objects.get_or_create(name=name, defaults={'content': name})
            content = markdownify(block.content)
            cache.set(cache_key, content, timeout=cls.CACHE_EXPIRE_TIME)

        return mark_safe(content)
