from django.contrib import admin

from markdownx.admin import MarkdownxModelAdmin

from .models import ContentBlock


class ContentBlockAdmin(MarkdownxModelAdmin):
    actions = None  # Avoid mass deleting which doesn't call delete() and bust cache


admin.site.register(ContentBlock, ContentBlockAdmin)
