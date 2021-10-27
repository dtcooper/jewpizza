import datetime
import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import get_default_timezone, get_default_timezone_name

from recurrence.fields import RecurrenceField
from s3direct.fields import S3DirectField

from jew_pizza.utils import format_date_short

from .constants import SHOW_CHOICES
from .utils import ffprobe, today_in_default_timezone


class ShowBaseModel(models.Model):
    name = models.CharField(
        max_length=255,
        blank=True,
        help_text=(
            "A blank value defaults to the name of the show, which is a sane default. Specify something here to"
            " override that, ie for podcasts, named or special shows."
        ),
    )
    show = models.CharField(max_length=max(len(c) for c, _ in SHOW_CHOICES), choices=SHOW_CHOICES)
    published = models.BooleanField(
        default=True, help_text="Whether to show this entry on the actual website. Leave unchecked for draft mode."
    )

    class Meta:
        abstract = True


class ShowDate(ShowBaseModel):
    start_time = models.TimeField("start time", help_text=f"Time in <strong>{get_default_timezone_name()}</strong>.")
    duration = models.DurationField(help_text="In <code>HH:MM:SS</code> format.")
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


class EpisodeManager(models.Manager):
    def get_by_natural_key(self, guid):
        return self.get(guid=guid)


class Episode(ShowBaseModel):
    date = models.DateField(
        "date", default=today_in_default_timezone, help_text=f"Time in <strong>{get_default_timezone_name()}</strong>."
    )
    duration = models.DurationField(
        default=datetime.timedelta(0),
        help_text="In <code>HH:MM:SS</code> format. Leave 00:00:00 to autofill from file.",
    )
    description = models.TextField(blank=True)
    guid = models.UUIDField(default=uuid.uuid4, unique=True, help_text="GUID for podcast. Automatically generated.")
    asset_url = S3DirectField(
        "audio asset",
        dest="show_asset_url",
        help_text="Upload audio asset here directly to DigitalOcean Spaces (S3). In mp3 format only.",
    )

    objects = EpisodeManager()

    def natural_key(self):
        return (self.guid,)

    class Meta:
        ordering = ('-date', 'show')
        indexes = (
            models.Index(fields=("date",)),
            models.Index(fields=("show", "date")),
        )

    @property
    def ffprobe(self):
        if not hasattr(self, "_ffprobe_cached") or self._ffprobe_cached[0] != self.asset_url:
            self._ffprobe_cached = (self.asset_url, ffprobe(self.asset_url))
        return self._ffprobe_cached[1]

    def clean(self):
        super().clean()

        # Rewrite URL (should happen before ffprobe call, to use caching)
        if self.asset_url.startswith(settings.AWS_S3_ENDPOINT_URL):
            self.asset_url = self.asset_url.replace(
                f"{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}",
                settings.DIGITALOCEAN_SPACES_REWRITE_URL,
            )

        if self.ffprobe is None:
            raise ValidationError({"asset_url": "ffmpeg error when processing file. Are you sure it's valid?"})

        if not self.asset_url.lower().endswith(".mp3") or self.ffprobe.format != "mp3":
            raise ValidationError({"asset_url": f"File must be an MP3. Got {self.ffprobe.format}."})

        if self.duration == datetime.timedelta(0):
            self.duration = self.ffprobe.duration

    def __str__(self, show_times=True):
        s = ""
        if not self.published:
            s += "<DRAFT> "
        s += self.get_show_display()
        if self.name:
            s += f" / {self.name}"
        if show_times:
            s += f" ({format_date_short(self.date)})"
        return s
