import numpy as np
import re
from collections import Counter
from functools import cmp_to_key

from core import utils
from django.db import models
from django.db.models import Sum
from django.template.defaultfilters import slugify
from django.utils.functional import cached_property
from django_extensions.db.fields import json

course_num_pattern = re.compile('[A-Za-z]*([0-9]+)[A-Za-z]*')

class Term(models.Model):
    SPRING = 0
    SUMMER = 1
    FALL = 2
    SEASON_CHOICES = (
        (SPRING, "Spring"),
        (SUMMER, "Summer"),
        (FALL, "Fall"),
    )
    season = models.IntegerField(choices=SEASON_CHOICES)
    year = models.IntegerField()

    def __unicode__(self):
        return "{0} {1}".format(self.get_season_display(), self.year)

    class Meta:
        ordering = ['year', 'season']

class DivisionSet(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(default='')
    # data is a json field consisting exactly of
    # { 'divisions' : [ list of divisions ] }
    data = json.JSONField()

    def __unicode__(self):
        return self.name

    @property
    def divisions_verbose(self):
        return [Course.DIVISION_CHOICE_DICT[div] for div in self.data['divisions']]

    @property
    def divisions_str(self):
        return ', '.join(self.divisions_verbose)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(DivisionSet, self).save(*args, **kwargs)


class Discipline(models.Model):
    """
    A category to which multiple subjects belong, such as natural
    science or arts and humanities.
    """
    name = models.CharField(max_length=60)
    slug = models.SlugField(default='')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Discipline, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']


class Subject(models.Model):
    """
    A single academic subject, such as mathematics or French.
    """
    name = models.CharField(max_length=256)
    short_name = models.CharField(max_length=256, null=True)
    canonical = models.CharField(max_length=256, null=True)
    discipline = models.ForeignKey(Discipline, null=True)
    slug = models.SlugField(default='')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Subject, self).save(*args, **kwargs)  


class Stats(models.Model):
    """
    An abstract base class to hold statistics about a
    subject or discipline.
    """

    division_set = models.ForeignKey(DivisionSet)
    letter_grades = models.IntegerField(default=0)
    mean = models.FloatField(null=True)
    stdev = models.FloatField(null=True)
    distribution = json.JSONField(null=True)
    my_rank = models.IntegerField(default=0)
    rank_count = models.IntegerField(default=0)

    class Meta:
        abstract = True

    @property
    def formatted_distribution(self):
        return utils.format_distribution(self.distribution, self.letter_grades)


class DivisionStats(Stats):
    """
    Holds division-wide stats.
    """


class DisciplineStats(Stats):
    """
    Holds statistics about a discipline for a particular division.
    """

    discipline = models.ForeignKey(Discipline)

    def __unicode__(self):
        return '{}: {}'.format(self.discipline.name, self.division_set.name)

class SubjectStats(Stats):
    """
    Holds statistics about a subject for a particular division.
    """

    subject = models.ForeignKey(Subject)

    def __unicode__(self):
        return '{}: {}'.format(self.subject.name, self.division_set.name)

class Course(models.Model):
    """
    A single course belonging to a single division, with
    many sections offered over multiple terms.
    """
    LOWER = 0
    UPPER = 1
    GRADUATE = 2
    TEACHING = 3
    PROFESSIONAL = 4
    MASTERS = 5
    DOCTORAL = 6
    OTHER = 7
    DIVISION_CHOICES = (
        (LOWER, "Lower Division"),
        (UPPER, "Upper Division"),
        (GRADUATE, "Graduate"),
        (TEACHING, "Teaching"),
        (PROFESSIONAL, "Professional"),
        (MASTERS, "Master's Exam"),
        (DOCTORAL, "Doctoral Exam"),
        (OTHER, "Other")
    )
    DIVISION_CHOICE_DICT = dict(DIVISION_CHOICES)

    subject = models.ForeignKey(Subject)
    title = models.TextField()
    number = models.CharField(max_length=10)
    num_numerical_part = models.IntegerField(null=True)
    division = models.IntegerField(choices=DIVISION_CHOICES, default=OTHER)

    # Stats
    distribution = json.JSONField(null=True)
    letter_grades = models.IntegerField(default=0)
    mean = models.FloatField(null=True)
    stdev = models.FloatField(null=True)

    def __unicode__(self):
        return "{0} {1}".format(self.subject, self.number)

    @property
    def formatted_distribution(self):
        return utils.format_distribution(self.distribution, self.letter_grades)

    def save(self, *args, **kwargs):
        m = course_num_pattern.match(self.number)
        if m:
            self.num_numerical_part = int(m.group(1))
            if self.num_numerical_part < 100:
                self.division = self.LOWER
            elif self.num_numerical_part < 200:
                self.division = self.UPPER
            elif self.num_numerical_part < 300:
                self.division = self.GRADUATE
            elif self.num_numerical_part < 400:
                self.division = self.TEACHING
            elif self.num_numerical_part < 500:
                self.division = self.PROFESSIONAL
            elif self.num_numerical_part == 601:
                self.division = self.MASTERS
            elif self.num_numerical_part == 602:
                self.division = self.DOCTORAL
            else:
                self.division = self.OTHER
        else:
            self.division = self.OTHER
        super(Course, self).save(*args, **kwargs)

    class Meta:
        ordering = ['subject', 'num_numerical_part', 'number']


class Section(models.Model):
    """
    A particular term's offering of a course, with a unique CCN.
    """
    course = models.ForeignKey(Course)
    term = models.ForeignKey(Term)
    number = models.CharField(max_length=10)
    instructor = models.CharField(max_length=1024)
    ccn = models.CharField(max_length=5, verbose_name="CCN")

    # Stats
    distribution = json.JSONField(null=True)
    letter_grades = models.IntegerField(default=0)
    mean = models.FloatField(null=True)
    stdev = models.FloatField(null=True)

    def __unicode__(self):
        return "{0}-{1} ({2})".format(self.course, self.number, self.term)

    class Meta:
        ordering = ['term', 'number']


class Grade(models.Model):
    """
    A type of grade, for example, A+ or PASS.
    """
    name = models.CharField(max_length=20)
    letter = models.BooleanField(default=False)
    points = models.FloatField(null=True, blank=True)

    def __unicode__(self):
        return self.name

class GradeCountManager(models.Manager):
    use_for_related_fields = True

    def in_grade_order(self, *args, **kwargs):
        qs = self.get_queryset().filter(*args, **kwargs)
        return sorted(qs, key = cmp_to_key(cmp_gc), reverse = True)

class GradeCount(models.Model):
    section = models.ForeignKey(Section)
    grade = models.ForeignKey(Grade)
    count = models.IntegerField()

    def __unicode__(self):
        return "GradeCount({0}, {1})".format(self.section, self.grade)

    objects = GradeCountManager()

def grade_order_key(grade_name):
    ordering = ['A+', 'A', 'A-', 'B+', 'B', 'B-',
                'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F',
                'High Honors', 'Honors',
                'Pass', 'Pass Conditional',
                'Credit', 'Satisfactory',
                'No Credit', 'Not Pass', 'Unsatisfactory']
    if grade_name not in ordering:
        return -1
    return ordering.index(grade_name)

def cmp_grade(grade1, grade2):
    """Return 0 for equal grades, 1 if grade1 > grade2, or -1 if grade1 < grade2."""
    if grade1 == grade2:
        return 0
    elif grade1.letter and not grade2.letter:
        return 1
    elif grade2.letter and not grade1.letter:
        return -1
    else:
        idx1 = grade_order_key(grade1.name)
        idx2 = grade_order_key(grade2.name)
        if idx1 == idx2:
            return 0
        elif idx1 < idx2:
            return 1
        else:
            return -1

def cmp_gc(gc1, gc2):
    return cmp_grade(gc1.grade, gc2.grade)
