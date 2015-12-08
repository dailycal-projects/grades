# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField()),
                ('number', models.CharField(max_length=10)),
                ('num_numerical_part', models.IntegerField(null=True)),
                ('division', models.IntegerField(default=7, choices=[(0, b'Lower Division'), (1, b'Upper Division'), (2, b'Graduate'), (3, b'Teaching'), (4, b'Professional'), (5, b"Master's Exam"), (6, b'Doctoral Exam'), (7, b'Other')])),
                ('distribution', django_extensions.db.fields.json.JSONField(null=True)),
                ('letter_grades', models.IntegerField(default=0)),
                ('mean', models.FloatField(null=True)),
                ('stdev', models.FloatField(null=True)),
            ],
            options={
                'ordering': ['subject', 'num_numerical_part', 'number'],
            },
        ),
        migrations.CreateModel(
            name='Discipline',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('slug', models.SlugField(default=b'')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='DisciplineStats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('letter_grades', models.IntegerField(default=0)),
                ('mean', models.FloatField(null=True)),
                ('stdev', models.FloatField(null=True)),
                ('distribution', django_extensions.db.fields.json.JSONField(null=True)),
                ('my_rank', models.IntegerField(default=0)),
                ('rank_count', models.IntegerField(default=0)),
                ('discipline', models.ForeignKey(to='core.Discipline')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DivisionSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('slug', models.SlugField(default=b'')),
                ('data', django_extensions.db.fields.json.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='DivisionStats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('letter_grades', models.IntegerField(default=0)),
                ('mean', models.FloatField(null=True)),
                ('stdev', models.FloatField(null=True)),
                ('distribution', django_extensions.db.fields.json.JSONField(null=True)),
                ('my_rank', models.IntegerField(default=0)),
                ('rank_count', models.IntegerField(default=0)),
                ('division_set', models.ForeignKey(to='core.DivisionSet')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('letter', models.BooleanField(default=False)),
                ('points', models.FloatField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='GradeCount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.IntegerField()),
                ('grade', models.ForeignKey(to='core.Grade')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=10)),
                ('instructor', models.CharField(max_length=1024)),
                ('ccn', models.CharField(max_length=5, verbose_name=b'CCN')),
                ('distribution', django_extensions.db.fields.json.JSONField(null=True)),
                ('letter_grades', models.IntegerField(default=0)),
                ('mean', models.FloatField(null=True)),
                ('stdev', models.FloatField(null=True)),
                ('course', models.ForeignKey(to='core.Course')),
            ],
            options={
                'ordering': ['term', 'number'],
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('canonical', models.CharField(max_length=256, null=True)),
                ('slug', models.SlugField(default=b'')),
                ('discipline', models.ForeignKey(to='core.Discipline', null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='SubjectStats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('letter_grades', models.IntegerField(default=0)),
                ('mean', models.FloatField(null=True)),
                ('stdev', models.FloatField(null=True)),
                ('distribution', django_extensions.db.fields.json.JSONField(null=True)),
                ('my_rank', models.IntegerField(default=0)),
                ('rank_count', models.IntegerField(default=0)),
                ('division_set', models.ForeignKey(to='core.DivisionSet')),
                ('subject', models.ForeignKey(to='core.Subject')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('season', models.IntegerField(choices=[(0, b'Spring'), (1, b'Summer'), (2, b'Fall')])),
                ('year', models.IntegerField()),
            ],
            options={
                'ordering': ['year', 'season'],
            },
        ),
        migrations.AddField(
            model_name='section',
            name='term',
            field=models.ForeignKey(to='core.Term'),
        ),
        migrations.AddField(
            model_name='gradecount',
            name='section',
            field=models.ForeignKey(to='core.Section'),
        ),
        migrations.AddField(
            model_name='disciplinestats',
            name='division_set',
            field=models.ForeignKey(to='core.DivisionSet'),
        ),
        migrations.AddField(
            model_name='course',
            name='subject',
            field=models.ForeignKey(to='core.Subject'),
        ),
    ]
