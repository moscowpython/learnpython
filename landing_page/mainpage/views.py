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
        'curators_list': curators_list,
        'graduate_stories': graduate_stories_list,
        'podcasts_list': podcasts_list,
        'today': date.today(),
        'is_online_closed': is_online_closed,
        'is_offline_closed': is_offline_closed,

    }
    return HttpResponse(template.render(context, request))


def projects(request):
    '''Docstring testc'''
    template = loader.get_template('mainpage/projects.html')

    # Student projects data
    student_projects_videos = list(GraduateProjectsVideos.objects.all().order_by('-project_course'))

    context = {
        'student_projects': student_projects_videos,
        'today': date.today()

    }
    return HttpResponse(template.render(context, request))
