import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import get_default_timezone

from recurrence.fields import RecurrenceField


class Show(models.Model):
    name = models.CharField("name", max_length=255)
    render_as_page = models.BooleanField(
        "render as page",
        blank=False,
        default=True,
        help_text="Render this show as its own page, and not just on the schedule.",
    )
    slug = models.SlugField("URL slug", blank=True, help_text="Required if 'render as page' is set.")
    start = models.TimeField("start time")
    duration = models.DurationField("duration")
    dates = RecurrenceField("dates", blank=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.render_as_page and not self.slug:
            raise ValidationError({"slug": "A slug is required when 'render as page' is set."})

        super().clean()

    def next_date_ranges(self, num=25, from_dt=None):
        if from_dt is None:
            from_dt = datetime.datetime.now()

        from_dt = from_dt.replace(microsecond=0)
        earliest_start = from_dt - self.duration
        tz = get_default_timezone()

        date_ranges = []
        for date in self.dates.occurrences(earliest_start):
            date = date.replace(hour=self.start.hour, minute=self.start.minute, second=self.start.second)
            if date >= earliest_start:
                date_ranges.append((tz.localize(date), tz.localize(date + self.duration)))
                if len(date_ranges) >= num:
                    break

        return date_ranges
