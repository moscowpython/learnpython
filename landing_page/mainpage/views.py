from datetime import date

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Curators, Enrollment, GraduateProjects


def index(request: HttpRequest) -> HttpResponse:
    enrollment = Enrollment.get_enrollment_with_active_registration()
    context = {
        'enrollment': enrollment,
        'projects': GraduateProjects.objects.all(),
        'registration_closes_date_formatted': enrollment.end_registration_date.strftime('%b %d, %Y %H:%M:%S'),
        'student_videos': [
            {
                'title': 'Путь джуна — из геодезиста в Support Engineer',
                'youtube_id': 'YySKSlNHDXo',
            },
            {
                'title': 'Как становятся джунами в британской компании на удалёнке',
                'youtube_id': 'TsqEigK2WQk',
            },
            {
                'title': 'Python-стрим - вход джуниора в АйТи',
                'youtube_id': 'wvijeR-eINA',
            },
            {
                'title': 'Как войти в разработку за считанные месяцы',
                'youtube_id': 'DkHWpgctTuA',
            },
            {
                'title': 'Личный опыт джуниора: удачи, фейлы, рецепты',
                'youtube_id': 'vKKqsJ8IvAg',
            },
            {
                'title': 'Python для врача и медицина для программиста.',
                'youtube_id': 's_ZNqjIW3ZA',
            }
        ],
        'curators_list': Curators.objects.filter(is_visible=True),
        'today': date.today(),
    }
    return render(request, 'mainpage/index.html', context)
