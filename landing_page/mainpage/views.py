from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import datetime
from .models import (MoscowPythonMeetup, LearnPythonCourse, GraduateProjects,
                     LearnPythonCoursePrices, Feedback, Curators, GraduateStories)


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

    # Program dates data
    course_day_2_date = LearnPythonCourse.objects.all()[:1].get().course_day_2
    course_day_3_date = LearnPythonCourse.objects.all()[:1].get().course_day_3
    course_day_4_date = LearnPythonCourse.objects.all()[:1].get().course_day_4
    course_day_5_date = LearnPythonCourse.objects.all()[:1].get().course_day_5
    course_day_6_date = LearnPythonCourse.objects.all()[:1].get().course_day_6
    course_day_7_date = LearnPythonCourse.objects.all()[:1].get().course_day_7
    course_day_8_date = LearnPythonCourse.objects.all()[:1].get().course_day_8
    course_day_9_date = LearnPythonCourse.objects.all()[:1].get().course_day_9

    # Time for lessons
    lesson_start_time = LearnPythonCourse.objects\
        .all()[:1].get().time_lessons_start
    lesson_end_time = LearnPythonCourse.objects\
        .all()[:1].get().offline_session_end

    # User stories
    graduate_stories_list = list(GraduateStories.objects.all())

    # Curators data
    curators_list = Curators.objects.filter(curator_status=True)

    # Feedback data
    student_feedback = list(Feedback.objects.all())

    # Meetup data
    # Fixes #3 MoscowPythonMeetup matching query does not exist.
    try:
        current_meetup = MoscowPythonMeetup.objects.latest('meetup_number')
    except MoscowPythonMeetup.DoesNotExist:
        current_meetup = MoscowPythonMeetup()

    context = {
        'meetup': current_meetup,
        'course': current_course,
        'projects': student_projects,
        'online_price_ranges': online_prices,
        'offline_price_ranges': offline_prices,
        'lesson_start_time': lesson_start_time,
        'lessons_end_time': lesson_end_time,
        'registration_closes_date': current_course.end_registration_date
        .strftime(
                '%b %d, %Y %H:%M:%S'
            ),
        'student_feedback': student_feedback,
        'curators_list': curators_list,
        'graduate_stories': graduate_stories_list

    }
    return HttpResponse(template.render(context, request))


def online(request):
    return render(request, 'mainpage/page3759545.html')