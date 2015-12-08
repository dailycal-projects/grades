import os
import csv
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from core.models import Subject, Discipline

class Command(BaseCommand):
    help = "Maps department names to disciplines."

    def handle(self, *args, **options):
        path = os.path.join(settings.DATA_DIR, 'disciplines.csv')
        print "Importing disciplines from {}".format(path)

        with open(path, 'r') as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                subject = Subject.objects.get(name=row['db_name'])
                subject.canonical = row['canonical_name']

                discipline, created = Discipline.objects.get_or_create(name=row['discipline'])
                subject.discipline = discipline
                subject.save()
