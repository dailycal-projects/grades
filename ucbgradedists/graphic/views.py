import json
from django.shortcuts import get_object_or_404
from bakery.views import BuildableTemplateView
from django.shortcuts import render
from core import utils
from core.models import DivisionSet, SubjectStats


class GraphicView(BuildableTemplateView):
    build_path = 'index.html'
    template_name = 'graphic.html'

    def get_context_data(self, **kwargs):
        context = {}

        division = DivisionSet.objects.get(slug='undergraduate')

        courses = []
        subject_stats = SubjectStats.objects.filter(division_set=division) \
                .filter(letter_grades__gte=1000).order_by('mean')
        for stat in subject_stats:
            info = {}
            info['sub'] = stat.subject.name
            info['discipline'] = stat.subject.discipline.name
            info['avg'] = stat.mean
            info['grade'] = utils.lettergrade(stat.mean)
            info['std'] = stat.stdev
            info['num'] = stat.letter_grades
            info['dist'] = stat.formatted_distribution

            courses.append(info)

        context['data'] = json.dumps(courses)

        return context