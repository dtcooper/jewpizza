from django.conf import settings
from django.contrib import admin

from constance import config
from constance.admin import Config, ConstanceAdmin, ConstanceForm

from jew_pizza.signals import config_updated_in_admin


class ConstanceSignalForm(ConstanceForm):
    def save(self):
        before = {name: getattr(config, name) for name in settings.CONSTANCE_CONFIG}
        super().save()
        after = {name: getattr(config, name) for name in settings.CONSTANCE_CONFIG}
        changes = sorted(name for name in settings.CONSTANCE_CONFIG if before[name] != after[name])
        if changes:
            config_updated_in_admin.send(sender=config, changes=changes, before=before, after=after)


class ConstanceSignalAdmin(ConstanceAdmin):
    change_list_form = ConstanceSignalForm


admin.site.unregister([Config])
admin.site.register([Config], ConstanceSignalAdmin)
