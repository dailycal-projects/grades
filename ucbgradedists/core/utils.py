from math import sqrt
from django.conf import settings

letter_to_points = {
    'A+': 4,
    'A': 4,
    'A-': 3.7,
    'B+': 3.3,
    'B': 3,
    'B-': 2.7,
    'C+': 2.3,
    'C': 2,
    'C-': 1.7,
    'D+': 1.3,
    'D': 1,
    'D-': 0.7,
    'F': 0
}

def distribution_stats(distribution):
    """
    Calculate the mean, standard deviation, and count
    for a letter grade distribution.
    """
    weighted_sum = 0
    weighted_square = 0
    total_grades = 0
    for letter, count in distribution.items():
        points = letter_to_points[letter]
        weighted_sum += points * count
        weighted_square += (points ** 2) * count
        total_grades += count
    if total_grades > 0:
        mean = weighted_sum/total_grades
        variance = weighted_square/total_grades - mean ** 2

        if variance > 0:
            stdev = sqrt(variance)
        else:
            stdev = 0

        mean = round(mean, settings.PRECISION)
        stdev = round(stdev, settings.PRECISION)
    else:
        mean = 0
        stdev = 0

    return mean, stdev, total_grades

def lettergrade(value):
    """
    Maps grade point average to letter grade.
    """
    if value > 3.85:
        return 'A'
    elif value > 3.5:
        return 'A-'
    elif value > 3.15:
        return 'B+'
    elif value > 2.85:
        return 'B'
    elif value > 2.5:
        return 'B-'
    elif value > 2.15:
        return 'C+'
    elif value > 1.85:
        return 'C'
    elif value > 1.5:
        return 'C-'
    elif value > 1.15:
        return 'D+'
    elif value > 0.85:
        return 'D'
    elif value > 0.5:
        return 'D-'
    else:
        return 'F'

def format_distribution(distribution, letter_grades):
    """
    Format grade distribution for histogram.
    """
    dist = []
    for grade in letter_to_points.keys():
        obj = {}
        obj['label'] = grade
        count = distribution.get(grade)
        if count > 0:
            obj['amt'] = round(100 * count/letter_grades, 2)
        else:
            obj['amt'] = 0
        dist.append(obj)

    return dist
