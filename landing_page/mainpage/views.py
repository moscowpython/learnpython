from django.shortcuts import render
from django.conf import settings
from django.http import (
    HttpResponse, HttpResponseForbidden,
    HttpResponseServerError)
from django.template import loader
from .models import (LearnPythonCourse, GraduateProjects,
                     LearnPythonCoursePrices,
                     Feedback, Curators, GraduateStories, GraduateProjectsVideos,
                     Podcasts,)
from datetime import date
import json


def index(request):
    '''Docstring testc'''
    template = loader.get_template('mainpage/index.html')

    # Course data
    # Fixes #3 LearnPythonCourse matching query does not exist.
    try:
        current_course = LearnPythonCourse.objects.latest('course_index')
    except LearnPythonCourse.DoesNotExist:
        current_course = LearnPythonCourse()

    online_prices = LearnPythonCoursePrices.objects.filter(
        course_type='Online').order_by('price_range_price')
    offline_prices = LearnPythonCoursePrices.objects.filter(
        course_type='Offline').order_by('price_range_price')
    offline_prices_penza = LearnPythonCoursePrices.objects.filter(
        course_type='OfflinePenza').order_by('price_range_price')
    offline_prices_spb = LearnPythonCoursePrices.objects.filter(
        course_type='OfflineSpb').order_by('price_range_price')

    # Student projects data
    student_projects = list(GraduateProjects.objects.all())

    # User stories
    graduate_stories_list = list(GraduateStories.objects.all())

    # User podcasts
    podcasts_list = list(Podcasts.objects.all())

    # Curators data
    curators_list = Curators.objects.filter(curator_status=True)

    # Feedback data
    student_feedback = list(Feedback.objects.all())

    # Closed sessions
    is_online_closed = current_course.online_session_closed

    is_offline_closed = current_course.offline_session_closed

    offline_cities = [
         {
             'name': 'Москва',
             'coords': [55.755988, 37.643448],
             'early_date': '2021-03-31',
             'early_price': 36500,
             'early_installment_price': 3500,
             'basic_date': '2021-04-01',
             'basic_price': 36500,
             'basic_installment_price': 3500
         },
         {
             'name': 'Санкт-Петербург',
             'coords': [59.935800, 30.318139],
             'early_date': '2021-04-30',
             'early_price': 36500,
             'early_installment_price': 3500,
             'basic_date': '2021-05-01',
             'basic_price': 36500,
             'basic_installment_price': 3500
         },
         {
             'name': 'Екатеринбург',
             'coords': [56.826403, 60.614272],
             'early_date': '2021-05-31',
             'early_price': 36500,
             'early_installment_price': 3500,
             'basic_date': '2021-06-01',
             'basic_price': 36500,
             'basic_installment_price': 3500
         },
         {
             'name': 'Самара',
             'coords': [53.192632, 50.110934],
             'early_date': '2021-06-30',
             'early_price': 36500,
             'early_installment_price': 3500,
             'basic_date': '2021-07-01',
             'basic_price': 36500,
             'basic_installment_price': 3500
         },
         {
             'name': 'Тольятти',
             'coords': [53.503970, 49.424335],
             'early_date': '2021-07-31',
             'early_price': 36500,
             'early_installment_price': 3500,
             'basic_date': '2021-08-01',
             'basic_price': 36500,
             'basic_installment_price': 3500
         },
         {
             'name': 'Сызрань',
             'coords': [53.150426, 48.475794],
             'early_date': '2021-08-31',
             'early_price': 36500,
             'early_installment_price': 3500,
             'basic_date': '2021-09-01',
             'basic_price': 36500,
             'basic_installment_price': 3500
         },
         {
             'name': 'Казань',
             'coords': [55.795976, 49.111556],
             'early_date': '2021-09-30',
             'early_price': 36500,
             'early_installment_price': 3500,
             'basic_date': '2021-10-01',
             'basic_price': 36500,
             'basic_installment_price': 3500
         }
     ]

    context = {
        'course': current_course,
        'projects': student_projects,
        'online_price_ranges': online_prices,
        'offline_price_ranges': offline_prices,
        'offline_price_penza_ranges': offline_prices_penza,
        'offline_price_spb_ranges': offline_prices_spb,
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
        'graduate_stories': graduate_stories_list,
        'podcasts_list': podcasts_list,
        'today': date.today(),
        'is_online_closed': is_online_closed,
        'is_offline_closed': is_offline_closed,
        'offline_cities': offline_cities,
        'offline_cities_json': json.dumps(offline_cities)
    }
    return HttpResponse(template.render(context, request))


def projects(request):
    '''Docstring testc'''
    template = loader.get_template('mainpage/projects.html')

    try:
        current_course = LearnPythonCourse.objects.latest('course_index')
    except LearnPythonCourse.DoesNotExist:
        current_course = LearnPythonCourse()

    # Student projects data
    student_projects_videos = list(GraduateProjectsVideos.objects.all().order_by('-project_course'))

    context = {
        'course': current_course,
        'student_projects': student_projects_videos,
        'today': date.today()

    }
    return HttpResponse(template.render(context, request))
