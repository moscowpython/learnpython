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
    current_course = LearnPythonCourse.objects.latest('course_index')
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

    # User stories
    graduate_stories_list = list(GraduateStories.objects.all())

    # Curators data
    curators_list = Curators.objects.filter(curator_status=True)

    # Feedback data
    student_feedback = list(Feedback.objects.all())

    # Meetup data
    current_meetup = MoscowPythonMeetup.objects.latest('meetup_number')

    context = {
        'meetup': current_meetup,
        'course': current_course,
        'projects': student_projects,
        'online_price_ranges': online_prices,
        'offline_price_ranges': offline_prices,
        'course_day_1': current_course.course_start_date.strftime('%d.%m'),
        'course_day_2': course_day_2_date.strftime('%d.%m'),
        'course_day_3': course_day_3_date.strftime('%d.%m'),
        'course_day_4': course_day_4_date.strftime('%d.%m'),
        'course_day_5': course_day_5_date.strftime('%d.%m'),
        'course_day_6': course_day_6_date.strftime('%d.%m'),
        'course_day_7': course_day_7_date.strftime('%d.%m'),
        'course_day_8': course_day_8_date.strftime('%d.%m'),
        'course_day_9': course_day_9_date.strftime('%d.%m'),
        'course_day_10': current_course.course_end_date.strftime('%d.%m'),
        'registration_closes_date': current_course.end_registration_date.strftime(
            '%b %d, %Y %H:%M:%S'
        ),
        'student_feedback': student_feedback,
        'curators_list': curators_list,
        'graduate_stories': graduate_stories_list

    }
    return HttpResponse(template.render(context, request))
