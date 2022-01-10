import json
import logging
import os
import subprocess

import requests

from huey.contrib import djhuey


logger = logging.getLogger(f"jewpizza.{__name__}")


@djhuey.task()
def generate_peaks(episode):
    episode.refresh_from_db()

    logger.info(f"Generating peaks for {episode.asset_url}")
    response = requests.get(episode.asset_url, stream=True)
    response.raise_for_status()

    file_format = os.path.splitext(episode.asset_url)[1].removeprefix(".")
    command = [
        "/usr/local/bin/audiowaveform",
        "--input-format",
        file_format,
        "-i",
        "-",
        "--output-format",
        "json",
        "-o",
        "-",
        "--pixels-per-second",
        "1",
        "--bits",
        "8",
    ]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

    for chunk in response.iter_content(8 * 1024):
        process.stdin.write(chunk)

    stdout, _ = process.communicate()
    peaks = json.loads(stdout)["data"]

    max_val = float(max(peaks))
    peaks = [round(x / max_val, 2) for x in peaks]

    episode.refresh_from_db()
    episode.peaks = peaks
    episode.save()
