import subprocess
import threading

from django.contrib.staticfiles.management.commands.runserver import Command as RunserverCommand


class Command(RunserverCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            '--without-npm-watch', action="store_false", dest="with_npm_watch",
            help="Do NOT run 'npm run watch' in a seprate thread",
        )

    def inner_run(self, *args, **options):
        if options['with_npm_watch']:
            self.stdout.write("Running tailwind (npm run watch)")
            thread = threading.Thread(target=subprocess.run, args=(['npm', '--prefix=../frontend', 'run', 'watch'],),
                                      kwargs={'check': True})
            thread.start()
        super().inner_run(*args, **options)
