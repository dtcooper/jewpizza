import datetime

from django.db import models
from django.utils.timezone import get_default_timezone

from recurrence.fields import RecurrenceField


class Show(models.Model):
    PROTECTED_SLUGS = (
        'showgram',
        'this-is-going-well-i-think',
        'that-went-well-i-think',
        'bmir',
    )

    name = models.CharField("name", max_length=255)
    slug = models.SlugField("URL slug", blank=True, help_text="Required if 'render as page' is set.", unique=True)

    def __str__(self):
        return self.name

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


class ShowDate(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='dates')
    start = models.TimeField("start time")
    duration = models.DurationField()
    dates = RecurrenceField()

    def __str__(self):
        return str(self.show)
