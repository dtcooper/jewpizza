from django.conf import settings
from django.contrib import admin

from constance import config
from constance.admin import Config, ConstanceAdmin, ConstanceForm

from jew_pizza.signals import config_updated_in_admin


class ConstanceSignalForm(ConstanceForm):
    def __init__(self, initial, request=None, *args, **kwargs):
        self._request = request
        super().__init__(initial=initial, request=request, *args, **kwargs)

    def save(self):
        before = {name: getattr(config, name) for name in settings.CONSTANCE_CONFIG}
        super().save()
        after = {name: getattr(config, name) for name in settings.CONSTANCE_CONFIG}
        changes = sorted(name for name in settings.CONSTANCE_CONFIG if before[name] != after[name])
        if changes:
            config_updated_in_admin.send(
                sender=config, changes=changes, before=before, after=after, request=self._request
            )


class ConstanceSignalAdmin(ConstanceAdmin):
    def get_changelist_form(self, request, **kwargs):
        class RequestConstanceSignalForm(ConstanceSignalForm):
            # Hack to make sure request gets passed to form always without modifying constance
            def __new__(cls, *args, **kwargs):
                kwargs.setdefault("request", request)
                return ConstanceSignalForm(*args, **kwargs)

        return RequestConstanceSignalForm


admin.site.unregister([Config])
admin.site.register([Config], ConstanceSignalAdmin)
