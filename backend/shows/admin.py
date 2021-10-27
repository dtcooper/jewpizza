from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Episode, ShowDate


class ShowsCommonModelAdminMixin:
    list_filter = ("published", "show")
    list_display_links = ("show", "display_name")

    @admin.display(description="Name", ordering="name", empty_value='asdf')
    def display_name(self, obj):
        return obj.name or mark_safe('<em>Untitled</em>')

    def get_fields(self, request, obj=None):
        fields = list(super().get_fields(request, obj=obj))
        if obj is None:
            for field in self.get_readonly_fields(request, obj=obj):
                fields.remove(field)

        return fields


class EpisodeAdminModelForm(forms.ModelForm):
    name_from_ffprobe = forms.BooleanField(
        label="Generate name from file's metadata.",
        required=False,
        help_text=(
            'Attempt to extract name from metadata on save. Will attempt to do so in <strong>"artist - title"</strong>'
            " format."
        ),
    )

class EpisodeAdmin(ShowsCommonModelAdminMixin, admin.ModelAdmin):
    form = EpisodeAdminModelForm
    fields = ("published", "show", "name", "name_from_ffprobe", "asset_url", "date", "duration", "guid")
    readonly_fields = ("guid",)
    list_display = ("published", "show", "display_name", "date", "date", "duration")

    def save_model(self, request, obj, form, change):
        if form.cleaned_data["name_from_ffprobe"]:
            obj.name = " - ".join(filter(None, (obj.ffprobe.artist, obj.ffprobe.title)))
        super().save_model(request, obj, form, change)


class ShowDateAdmin(ShowsCommonModelAdminMixin, admin.ModelAdmin):
    fields = ("show", "published", "name", "dates", "start_time", "duration", "end_time")
    list_display = ("published", "show", "display_name", "start_time", "end_time", "duration")
    readonly_fields = ("end_time",)

    @admin.display(description="Show name", ordering="show")
    def display_show(self, obj):
        return obj.__str__(show_times=False)


admin.site.register(Episode, EpisodeAdmin)
admin.site.register(ShowDate, ShowDateAdmin)
