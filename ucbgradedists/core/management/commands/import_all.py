import glob
from django.conf import settings
from django.core.management.base import BaseCommand
from core.models import *
from import_csv import create_objects


class Command(BaseCommand):
    help = """
    Imports grade distribution data from the DATA_DIR.
    File names should be of the form '[season][year].csv', where [season] is
    one of 'fa', 'sp', 'su' (for Fall, Spring, and Summer).
    """

    def handle(self, *args, **options):
        print('Importing data from {}'.format(settings.DATA_DIR))
        prefixes = ['sp', 'su', 'fa']
        paths = [
            glob.glob(settings.DATA_DIR + '/sp*.csv'),
            glob.glob(settings.DATA_DIR + '/su*.csv'),
            glob.glob(settings.DATA_DIR + '/fa*.csv'),
        ]
        processed_paths = 0
        total_paths = sum([len(path_list) for path_list in paths])
        for season, path_list in enumerate(paths):
            for path in path_list:
                year = int(path.split(prefixes[season])[-1][:4])
                create_objects(season, year, path)
                processed_paths += 1
                print("import_dir: processed {0} ({1} of {2})".\
                    format(path, processed_paths, total_paths))
