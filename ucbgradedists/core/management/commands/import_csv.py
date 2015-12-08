import csv
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from core.models import *

class Command(BaseCommand):
    help = "Imports grade distribution data from a Cal Answers CSV file"

    def add_arguments(self, parser):
        parser.add_argument('season', type=int, help="season (0: spring, 1: summer, 2: fall)")
        parser.add_argument('year', type=int, help="academic year")
        parser.add_argument('inname', help="path to the csv file to read")

    def handle(self, *args, **options):
        verbosity = options['verbosity']
        term = create_objects(options['season'], options['year'],
                              options['inname'])

def create_objects(season, year, inname, verbosity=1):
    # assumption: this csv only contains data for one term, so CCNs are unique
    term = Term.objects.get_or_create(season=season, year=year)[0]
    # data['sections'] maps CCN to a Section object
    data = {'sections': {}}
    with open(inname, 'r+') as infile:
        inreader = csv.reader(infile)
        indices = None
        processed = 0
        for row in inreader:
            if indices is None:
                header = [s.replace('\xef\xbb\xbf', '') for s in row]
                indices = find_indices(header)
                continue
            data = process_row(term, data, row, indices)
            processed += 1
            if verbosity >= 1:
                if processed % 10 == 0 or verbosity >= 3:
                    print "object creation: {} rows processed".format(processed)
    return term

def process_row(term, data, row, indices):
    """Find the section corresponding to ROW, create necessary objects,
    and add the grade count."""
    ccn = row[indices['ccn']]
    if ccn not in data['sections']:
        """
        Create all or any of the
        subject, course, section, grade, and grade count
        if they don't exist.
        """
        subject = Subject.objects.get_or_create(name=row[indices['subject']])[0]
        course = Course.objects.get_or_create(subject_id=subject.id,
                                              number=row[indices['course_num']])[0]
        course.title = row[indices['title']]
        course.save()
        section = Section.objects.get_or_create(course_id=course.id,
                                                term_id=term.id,
                                                number=row[indices['section_num']],
                                                instructor=row[indices['instructor']],
                                                ccn=ccn)[0]
        section.save()
        data['sections'][ccn] = section
    letter = row[indices['letter']] == "Letter Grade"
    points = row[indices['points']]
    points = float(points) if len(points) > 0 else None
    grade = Grade.objects.get_or_create(name=row[indices['grade_name']],
                                        letter=letter,
                                        points=points)[0]
    try:
        gradecount = GradeCount.objects.get(section_id=data['sections'][ccn].id, grade_id=grade.id)
    except ObjectDoesNotExist:
        gradecount = GradeCount(section=data['sections'][ccn], grade=grade)
    gradecount.count = int(row[indices['count']])
    gradecount.save()
    return data

def find_indices(header):
    """Return the positions of relevant fields in our rows."""
    return {
        'subject': header.index("Course Subject Short Nm"),
        'course_num': header.index("Course Number"),
        'section_num': header.index("Section Nbr"),
        'title': header.index("Course Title Nm"),
        'instructor': header.index("Instructor Name"),
        'ccn': header.index("Course Control Nbr"),
        'grade_name': header.index("Grade Nm"),
        'count': header.index("Enrollment Cnt"),
        'letter': header.index("Grade Type Desc"),
        'points': header.index("Average Grade"),
    }
