import os
import signal
import subprocess
import sys
import threading
import time

from django.conf import settings
from django.contrib.staticfiles.management.commands.runserver import Command as RunserverCommand
from django.core.management import CommandError
from django.utils.autoreload import DJANGO_AUTORELOAD_ENV


class Command(RunserverCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--without-npm-watch",
            action="store_false",
            dest="with_npm_watch",
            help="Do NOT run 'npm run watch' in a seprate thread",
        )

    def execute(self, *args, **options):
        self.exited = False

        if options["with_npm_watch"] and os.environ.get(DJANGO_AUTORELOAD_ENV) != "true":
            if sys.stdin.isatty():
                thread = threading.Thread(target=self.run_npm_watch)
                thread.start()
            else:
                raise CommandError(
                    "stdin is *NOT* a tty, can't run tailwind (npm run watch). Is docker-compose.dev.yml ->"
                    " docker-compose.override.yml symlinked?"
                )
        try:
            super().execute(*args, **options)
        finally:
            self.exited = True

    def run_npm_watch(self):
        while True:
            self.stdout.write("Running tailwind (npm run watch)")

            # stdin needs to be a pipe, since sharing it with parent breaks pdb
            process = subprocess.Popen(
                ["npm", "--prefix=../frontend", "run", "watch"],
                stdin=subprocess.PIPE,
                preexec_fn=os.setsid,
            )
            while process.poll() is None:
                if self.exited:  # Kill subprocess and all children when main thread exits
                    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                    return
                time.sleep(0.1)

            if process.returncode < 0:
                # negative = the child was terminated by signal N (POSIX only) - from subprocess manual
                return

            stylesheet = settings.BASE_DIR / "webcore" / "static" / "css" / "styles.css"
            if os.path.exists(stylesheet):
                os.remove(stylesheet)

            self.stderr.write("Tailwind crashed. Retrying in 1 second. (npm run watch)")
            time.sleep(1)
