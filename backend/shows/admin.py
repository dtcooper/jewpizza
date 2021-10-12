from django.contrib import admin

from .models import Show, ShowDate


class ShowDateInline(admin.TabularInline):
    model = ShowDate
    extra = 0


class ShowAdmin(admin.ModelAdmin):
    inlines = (ShowDateInline,)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj=obj)
        if obj is not None and obj.slug in Show.PROTECTED_SLUGS:
            readonly_fields = list(readonly_fields)
            readonly_fields.append('slug')
        return readonly_fields

    def has_delete_permission(self, request, obj=None):
        return obj is None or obj.slug not in Show.PROTECTED_SLUGS


admin.site.register(Show, ShowAdmin)
