from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Episode, ShowDate


class ShowsCommonModelAdminMixin:
    save_on_top = True
    list_filter = ("published", "show_code")
    list_display_links = ("show_code", "display_name")

    @admin.display(description="Name", ordering="name", empty_value=mark_safe("<em>Untitled</em>"))
    def display_name(self, obj):
        return obj.name or None

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
    fields = (
        "show_code",
        "published",
        "slug",
        "asset_url",
        "name",
        "name_from_ffprobe",
        "description",
        "date",
        "duration",
        "guid",
        "has_peaks",
    )
    readonly_fields = ("guid", "has_peaks")
    list_display = ("published", "show_code", "display_name", "date", "date", "duration", "has_peaks")

    @admin.display(description="Peaks", boolean=True)
    def has_peaks(self, obj):
        return bool(obj.peaks)

    def save_model(self, request, obj, form, change):
        if form.cleaned_data["name_from_ffprobe"]:
            obj.name = " - ".join(filter(None, (obj.ffprobe.artist, obj.ffprobe.title)))
        super().save_model(request, obj, form, change)


class ShowDateAdmin(ShowsCommonModelAdminMixin, admin.ModelAdmin):
    fields = ("show_code", "published", "name", "dates", "start_time", "duration", "end_time")
    list_display = ("published", "show_code", "display_name", "start_time", "end_time", "duration")
    readonly_fields = ("end_time",)


admin.site.register(Episode, EpisodeAdmin)
admin.site.register(ShowDate, ShowDateAdmin)
