from collections import Counter

from django.conf import settings
from django.core.management import BaseCommand
from django.core import serializers

from shows.models import Show

import requests


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--auto', action='store_true', help='Automatically detect command should run or not.')

    def handle(self, *args, **options):
        if options['auto']:
            actual_count = Show.objects.filter(slug__in=Show.PROTECTED_SLUGS).count()
            if actual_count == len(Show.PROTECTED_SLUGS):
                return

            self.stdout.write("Detected incomplete show list. Sync'ing show list.")

        url = settings.LOAD_SHOWS_DEV_EXPORT_URL
        data = requests.get(url).text
        objs = serializers.deserialize('json', data)

        Show.objects.all().delete()

        count = 0
        for obj in objs:
            obj.save()
            if isinstance(obj.object, Show):
                count += 1

        self.stdout.write(f'{count} shows created from {url}')
