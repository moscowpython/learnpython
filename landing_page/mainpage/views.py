from django.http import HttpResponse
from django.template import loader
from .models import (LearnPythonCourse, GraduateProjects,
                     LearnPythonCoursePrices,
                     Feedback, Curators, GraduateProjectsVideos
                     )
from datetime import date


def index(request):
    template = loader.get_template('mainpage/index.html')

    try:
        current_course = LearnPythonCourse.objects.latest('course_index')
    except LearnPythonCourse.DoesNotExist:
        current_course = LearnPythonCourse()

    online_prices = LearnPythonCoursePrices.objects.filter(
        course_type='Online').order_by('price_range_price')

    # Student projects data
    student_projects = list(GraduateProjects.objects.all())

    # Curators data
    curators_list = Curators.objects.filter(curator_status=True)

    # Feedback data
    student_feedback = list(Feedback.objects.all())

    context = {
        'course': current_course,
        'projects': student_projects,
        'online_price_ranges': online_prices,
        'registration_closes_date': current_course.end_registration_date
        .strftime(
                '%b %d, %Y %H:%M:%S'
            ),
        'student_feedback': student_feedback,
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
        'curators_list': curators_list,
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
