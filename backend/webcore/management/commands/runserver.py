import subprocess
import sys
import threading

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

    def inner_run(self, *args, **options):
        if options["with_npm_watch"]:
            self.stdout.write("Running tailwind (npm run watch)")
            thread = threading.Thread(
                target=subprocess.run, args=(["npm", "--prefix=../frontend", "run", "watch"],), kwargs={"check": True}
            )
            thread.start()
        super().inner_run(*args, **options)
