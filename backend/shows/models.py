from django.db import models

from recurrence.fields import RecurrenceField

from .constants import SHOW_CHOICES


class ShowDate(models.Model):
    name = models.CharField(max_length=255, blank=True, help_text="Leave blank for the default, a non-special show.")
    show = models.CharField(max_length=max(len(c) for c, _ in SHOW_CHOICES), choices=SHOW_CHOICES)
    start = models.TimeField("start time")
    duration = models.DurationField()
    dates = RecurrenceField()

    def __str__(self):
        s = f"Show dates for {self.get_show_display()}"
        if self.name:
            s += f" - {self.name}"
        return s
