import os
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Load data and compute statistics."

    def handle(self, *args, **options):
        call_command('import_all')
        call_command('import_disciplines')
        call_command('compute_stats')
