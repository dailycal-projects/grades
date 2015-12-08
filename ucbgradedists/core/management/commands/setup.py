import os
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Load data and compute statistics."

    def handle(self, *args, **options):
        call_command('import_dir', settings.DATA_DIR)
        call_command('import_disciplines',
                     os.path.join(settings.DATA_DIR, 'disciplines.csv'))
        call_command('compute_stats')
