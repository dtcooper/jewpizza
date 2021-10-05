from django.contrib import admin

from .models import SignUp, TextMessage


class TextMessageAdmin(admin.ModelAdmin):
    date_hierarchy = "created"
    list_display = ("phone", "created", "message")
    search_fields = ("phone",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(TextMessage, TextMessageAdmin)
admin.site.register(SignUp)
