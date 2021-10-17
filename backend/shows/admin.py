from django.contrib import admin
from django.db.models import DurationField

from durationwidget.widgets import TimeDurationWidget

from jew_pizza.utils import format_datetime_short

from .models import Episode, ShowDate


class ShowsCommonModelAdminMixin:
    list_display_links = ("display_show",)
    list_filter = ("published", "show")

    formfield_overrides = {
        DurationField: {"widget": TimeDurationWidget(show_days=False, show_seconds=False)},
    }

    @admin.display(description="Show", ordering="show")
    def display_show(self, obj):
        return obj.__str__(show_times=False)


class EpisodeAdmin(ShowsCommonModelAdminMixin, admin.ModelAdmin):
    fields = ("show", "published", "name", "asset_url", "start", "duration", "end_display")
    list_display = ("published", "display_show", "start", "end", "duration")
    readonly_fields = ("end_display",)

    @admin.display(description="end date")
    def end_display(self, obj):
        if obj.end:
            return format_datetime_short(obj.end)


class ShowDateAdmin(ShowsCommonModelAdminMixin, admin.ModelAdmin):
    fields = ("show", "published", "name", "start_time", "duration", "end_time")
    list_display = ("published", "display_show", "start_time", "end_time", "duration")
    readonly_fields = ("end_time",)


admin.site.register(Episode, EpisodeAdmin)
admin.site.register(ShowDate, ShowDateAdmin)
