import datetime

from django.db import models

from recurrence.fields import RecurrenceField

from jew_pizza.utils import format_datetime_short

from .constants import SHOW_CHOICES


class ShowBaseModel(models.Model):
    name = models.CharField(
        max_length=255,
        blank=True,
        help_text="A blank value defaults to the name of the show (used for special content).",
    )
    show = models.CharField(max_length=max(len(c) for c, _ in SHOW_CHOICES), choices=SHOW_CHOICES)
    published = models.BooleanField(default=True)

    class Meta:
        abstract = True


class ShowDate(ShowBaseModel):
    start_time = models.TimeField("start time")
    duration = models.DurationField()
    dates = RecurrenceField()

    class Meta:
        ordering = ("id",)

    @property
    def end_time(self):
        if self.start_time:
            # Apply to Jan 1
            start_date = datetime.datetime.combine(datetime.date(datetime.date.today().year, 1, 1), self.start_time)
            return (start_date + self.duration).time()

    def __str__(self, show_times=True):
        s = ""
        if not self.published:
            s += "<DRAFT> "
        s += self.get_show_display()
        if self.name:
            s += f" / {self.name}"
        if show_times:
            s += f" [{self.start_time} - {self.end_time}]"

        return s


class Episode(ShowBaseModel):
    asset_url = models.URLField()
    start = models.DateTimeField("start date", db_index=True)
    duration = models.DurationField()
    description = models.TextField()

    @property
    def end(self):
        if self.start:
            return self.start + self.duration

    def __str__(self, show_times=True):
        s = ""
        if not self.published:
            s += "<DRAFT> "
        s += self.get_show_display()
        if self.name:
            s += f" / {self.name}"
        if show_times:
            s += f" [{format_datetime_short(self.start)} - {format_datetime_short(self.end)}]"
        return s
