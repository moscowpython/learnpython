from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import datetime
from .models import MoscowPythonMeetup, LearnPythonCourse, GraduateProjects, LearnPythonCoursePrices, Feedback


def index(request):
    template = loader.get_template('mainpage/index.html')

    months_list = (
        'Января',
        'Февраля',
        'Марта',
        'Апреля',
        'Мая',
        'Июня',
        'Июля',
        'Августа',
        'Сентября',
        'Октября',
        'Ноября',
        'Декабря'
    )

    # Course data
    current_course = LearnPythonCourse.objects.latest('course_index')
    course_month_start = LearnPythonCourse.objects.all()[:1].get().course_start_date
    course_month_end = LearnPythonCourse.objects.all()[:1].get().course_end_date
    online_price = LearnPythonCoursePrices.objects.filter(course_type='Online').order_by('price_range_price')
    offline_price = LearnPythonCoursePrices.objects.filter(course_type='Offline').order_by('price_range_price')

    # Student projects data
    student_projects = list(GraduateProjects.objects.all())

    # Price range data
    today_date = datetime.datetime.today().date()
    if today_date < online_price[0].price_range_end_date:
        today_range = 1
    elif today_date < online_price[1].price_range_end_date:
        today_range = 2
    else:
        today_range = 3

    # Program dates data
    course_day_1_date = LearnPythonCourse.objects.all()[:1].get().course_start_date
    course_day_2_date = LearnPythonCourse.objects.all()[:1].get().course_day_2
    course_day_3_date = LearnPythonCourse.objects.all()[:1].get().course_day_3
    course_day_4_date = LearnPythonCourse.objects.all()[:1].get().course_day_4
    course_day_5_date = LearnPythonCourse.objects.all()[:1].get().course_day_5
    course_day_6_date = LearnPythonCourse.objects.all()[:1].get().course_day_6
    course_day_7_date = LearnPythonCourse.objects.all()[:1].get().course_day_7
    course_day_8_date = LearnPythonCourse.objects.all()[:1].get().course_day_8
    course_day_9_date = LearnPythonCourse.objects.all()[:1].get().course_day_9
    course_day_10_date = LearnPythonCourse.objects.all()[:1].get().course_end_date

    # Registation closure data
    registration_closes_date = LearnPythonCourse.objects.all()[:1].get().end_registration_date

    # Feedback data
    student_feedback = list(Feedback.objects.all())

    # Meetup data
    current_meetup = MoscowPythonMeetup.objects.latest('meetup_number')

    context = {
        'meetup': current_meetup,
        'course': current_course,
        'projects': student_projects,
        'lowest_online_course_price': online_price[0],
        'lowest_offline_course_price': offline_price[0],
        'course_day_start': course_month_start.day,
        'course_day_after_start': course_month_start.day + 1,
        'course_day_before_end': course_month_end.day - 1,
        'course_day_end': course_month_end.day,
        'course_month_start': months_list[course_month_start.month - 1],
        'course_month_end': months_list[course_month_end.month - 1],
        'course_day_1': course_day_1_date.strftime('%d.%m'),
        'course_day_2': course_day_2_date.strftime('%d.%m'),
        'course_day_3': course_day_3_date.strftime('%d.%m'),
        'course_day_4': course_day_4_date.strftime('%d.%m'),
        'course_day_5': course_day_5_date.strftime('%d.%m'),
        'course_day_6': course_day_6_date.strftime('%d.%m'),
        'course_day_7': course_day_7_date.strftime('%d.%m'),
        'course_day_8': course_day_8_date.strftime('%d.%m'),
        'course_day_9': course_day_9_date.strftime('%d.%m'),
        'course_day_10': course_day_10_date.strftime('%d.%m'),
        'today_range': today_range,
        'registration_closes_date': registration_closes_date.strftime('%b %d, %Y %H:%M:%S'),
        'student_feedback': student_feedback

    }
    return HttpResponse(template.render(context, request))
