import dataclasses
import datetime
from typing import Optional

from django.http import HttpResponse
from django.template import loader
from .models import (LearnPythonCourse, GraduateProjects,
                     Feedback, Curators, GraduateProjectsVideos
                     )
from datetime import date


@dataclasses.dataclass
class CoursePrice:
    price_rub: int
    date_from: Optional[datetime.date] = None
    date_to: Optional[datetime.date] = None


@dataclasses.dataclass
class Enrollment:
    timepad_event_id: str
    start_date: datetime.date
    end_date: datetime.date
    end_registration_date: datetime.date
    early_price: CoursePrice
    late_price: CoursePrice


def index(request):
    template = loader.get_template('mainpage/index.html')

    enrollment = Enrollment(
        timepad_event_id='2441413',
        start_date=datetime.date(2023, 9, 2),
        end_date=datetime.date(2023, 11, 4),
        end_registration_date=datetime.date(2023, 8, 31),
        early_price=CoursePrice(price_rub=30000, date_to=datetime.date(2023, 6, 30)),
        late_price=CoursePrice(price_rub=35000, date_from=datetime.date(2023, 7, 1)),
    )

    context = {
        'enrollment': enrollment,
        'projects': GraduateProjects.objects.all(),

        'registration_closes_date_formatted': enrollment.end_registration_date.strftime('%b %d, %Y %H:%M:%S'),
        'student_feedback': Feedback.objects.all(),
        'student_videos': [
            {
                'title': 'Как войти в разработку за считанные месяцы',
                'youtube_id': 'DkHWpgctTuA'
            },
            {
                'title': 'Личный опыт джуниора: удачи, фейлы, рецепты',
                'youtube_id': 'vKKqsJ8IvAg'
            },
            {
                'title': 'Python для врача и медицина для программиста.',
                'youtube_id': 's_ZNqjIW3ZA'
            }
        ],
        'curators_list': Curators.objects.filter(curator_status=True),
        'today': date.today(),
    }
    return HttpResponse(template.render(context, request))


def projects(request):
    template = loader.get_template('mainpage/projects.html')

    try:
        current_course = LearnPythonCourse.objects.latest('course_index')
    except LearnPythonCourse.DoesNotExist:
        current_course = LearnPythonCourse()

    student_projects_videos = list(GraduateProjectsVideos.objects.all().order_by('-project_course'))

    context = {
        'course': current_course,
        'student_projects': student_projects_videos,
        'today': date.today()

    }
    return HttpResponse(template.render(context, request))
