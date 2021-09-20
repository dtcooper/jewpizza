import os
import subprocess
import sys
import threading
import time

from django.conf import settings
from django.contrib.staticfiles.management.commands.runserver import Command as RunserverCommand
from django.core.management import CommandError


class Command(RunserverCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--without-npm-watch",
            action="store_false",
            dest="with_npm_watch",
            help="Do NOT run 'npm run watch' in a seprate thread",
        )

    def handle(self, *args, **options):
        if options["with_npm_watch"] and not sys.stdin.isatty():
            raise CommandError(
                "stdin is *NOT* a tty, can't run tailwind (npm run watch). Is docker-compose.dev.yml ->"
                " docker-compose.override.yml symlinked?"
            )
        super().handle(*args, **options)

    def run_npm_watch(self):
        def clear_stylesheet():
            try:
                os.remove(settings.BASE_DIR / "webcore" / "static" / "css" / "styles.css")
            except FileNotFoundError:
                return

        while True:
            self.stdout.write("Running tailwind (npm run watch)")
            try:
                clear_stylesheet()
                subprocess.run(["npm", "--prefix=../frontend", "run", "watch"], check=True)
            except subprocess.SubprocessError:
                clear_stylesheet()
                self.stderr.write("Tailwind crashed. Retrying in 1 second. (npm run watch)")
                time.sleep(1)

    def inner_run(self, *args, **options):
        if options["with_npm_watch"]:
            thread = threading.Thread(target=self.run_npm_watch)
            thread.start()
        super().inner_run(*args, **options)
