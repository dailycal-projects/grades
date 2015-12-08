import json
from collections import Counter
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
        overall_distribution = Counter()
        subject_stats = SubjectStats.objects.filter(division_set=division) \
                .filter(letter_grades__gte=1000).order_by('mean')
        for stat in subject_stats:
            info = {}
            info['sub'] = stat.subject.name
            info['slug'] = stat.subject.slug
            info['discipline'] = stat.subject.discipline.name
            info['avg'] = stat.mean
            info['grade'] = utils.lettergrade(stat.mean)
            info['std'] = stat.stdev
            info['num'] = stat.letter_grades
            info['dist'] = stat.formatted_distribution
            info['rank'] = stat.my_rank

            overall_distribution += Counter(stat.distribution)

            courses.append(info)

        context['data'] = json.dumps(courses)

        context['overall_avg'], context['overall_std'], context['overall_num'] \
         = utils.distribution_stats(overall_distribution)

        return context
