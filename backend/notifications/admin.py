from django.contrib import admin

from .models import TextMessage


class TextMessageAdmin(admin.ModelAdmin):
    save_on_top = True
    date_hierarchy = "created"
    list_display = ("phone_number", "created", "message")
    search_fields = ("phone_number",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(TextMessage, TextMessageAdmin)
