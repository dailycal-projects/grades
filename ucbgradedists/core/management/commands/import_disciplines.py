import os
import csv
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from core.models import Subject, Discipline

class Command(BaseCommand):
    help = "Maps department names to disciplines."

    def add_arguments(self, parser):
        parser.add_argument('path', help="path to the CSV file mapping departments to disciplines")

    def handle(self, *args, **options):
        print "Importing disciplines from {}".format(options['path'])
        with open(options['path'], 'r') as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                subject = Subject.objects.get(name=row['db_name'])
                subject.canonical = row['canonical_name']

                discipline, created = Discipline.objects.get_or_create(name=row['discipline'])
                subject.discipline = discipline
                subject.save()
