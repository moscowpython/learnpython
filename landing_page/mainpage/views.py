import hmac
from hashlib import sha1

from django.shortcuts import render
from django.conf import settings
from django.http import (
    HttpResponse, HttpResponseForbidden,
    HttpResponseServerError)
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.template import loader
from .models import (LearnPythonCourse, GraduateProjects,
                     LearnPythonCoursePrices,
                     Feedback, Curators, GraduateStories)
from datetime import date
from django.utils.encoding import force_bytes


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

    # Student projects data
    student_projects = list(GraduateProjects.objects.all())

    # User stories
    graduate_stories_list = list(GraduateStories.objects.all())

    # Curators data
    curators_list = Curators.objects.filter(curator_status=True)

    # Feedback data
    student_feedback = list(Feedback.objects.all())

    context = {
        'course': current_course,
        'projects': student_projects,
        'online_price_ranges': online_prices,
        'offline_price_ranges': offline_prices,
        'registration_closes_date': current_course.end_registration_date
        .strftime(
                '%b %d, %Y %H:%M:%S'
            ),
        'student_feedback': student_feedback,
        'curators_list': curators_list,
        'graduate_stories': graduate_stories_list,
        'student_projects': student_projects,
        'today': date.today()

    }
    return HttpResponse(template.render(context, request))
