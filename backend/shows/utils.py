from collections import namedtuple
import datetime
import json
import logging
import math
import subprocess

from django.utils.timezone import get_default_timezone


logger = logging.getLogger(f"jewpizza.{__file__}")
FFProbeData = namedtuple("FFProbeData", ("format", "duration", "artist", "title"))


def ffprobe(url):
    # We want at least one audio channel
    cmd = subprocess.run(
        [
            "ffprobe",
            "-i",
            url,
            "-print_format",
            "json",
            "-hide_banner",
            "-loglevel",
            "error",
            "-show_format",
            "-show_error",
            "-show_streams",
            "-select_streams",
            "a:0",
        ],
        text=True,
        capture_output=True,
    )

    kwargs = {}
    if cmd.returncode == 0:
        ffprobe_data = json.loads(cmd.stdout)
        if ffprobe_data and ffprobe_data["streams"] and ffprobe_data["format"]:
            kwargs.update(
                {
                    "format": ffprobe_data["format"]["format_name"],
                    "duration": datetime.timedelta(
                        seconds=math.ceil(float(ffprobe_data["streams"][0].get("duration") or 0))
                    ),
                }
            )
        else:
            logger.warning(f"ffprobe returned a bad or empty response: {cmd.stdout}")
            return None
    else:
        logger.warning(f"ffprobe returned {cmd.returncode}: {cmd.stderr}")
        return None

    ffprobe_tags = ffprobe_data["format"].get("tags", {})
    for field in ("artist", "title"):
        kwargs[field] = ffprobe_tags.get(field, "").strip()

    return FFProbeData(**kwargs)


def today_in_default_timezone():
    return datetime.datetime.now(get_default_timezone()).date()
