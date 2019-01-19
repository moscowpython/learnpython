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


def online(request):
    return render(request, 'mainpage/page3759545.html')


@csrf_exempt
@require_POST
def webhook(request):
    # Verify secret code
    header_signature = request.META.get('HTTP_X_HUB_SIGNATURE')
    if header_signature is None:
        return HttpResponseForbidden('Permission denied.')

    sha_name, signature = header_signature.split('=')
    if sha_name != 'sha1':
        return HttpResponseServerError('Operation not supported.', status=501)

    mac = hmac.new(
        force_bytes(settings.WEBHOOK_KEY),
        msg=force_bytes(request.body),
        digestmod=sha1
        )

    if not hmac.compare_digest(force_bytes(mac.hexdigest()), force_bytes(signature)):
        return HttpResponseForbidden('Permission denied.')

    # If request reached this point we are in a good shape
    return HttpResponse(status=200)
