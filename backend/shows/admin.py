from django.contrib import admin
from django.db.models import DurationField

from durationwidget.widgets import TimeDurationWidget

from .models import ShowDate


class ShowDateAdmin(admin.ModelAdmin):
    list_display = ("show", "start", "duration")

    formfield_overrides = {
        DurationField: {"widget": TimeDurationWidget(show_days=False)},
    }


admin.site.register(ShowDate, ShowDateAdmin)
