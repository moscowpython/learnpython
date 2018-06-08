from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import datetime
from .models import MoscowPythonMeetup, LearnPythonCourse, GraduateProjects, LearnPythonCoursePrices


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

    current_course = LearnPythonCourse.objects.latest('course_index')
    course_month_start = LearnPythonCourse.objects.all()[:1].get().course_start_date
    course_month_end = LearnPythonCourse.objects.all()[:1].get().course_end_date
    online_price = LearnPythonCoursePrices.objects.filter(course_type='Online').order_by('price_range_price')
    offline_price = LearnPythonCoursePrices.objects.filter(course_type='Offline').order_by('price_range_price')

    student_projects = list(GraduateProjects.objects.all())

    today_date = datetime.datetime.today().date()

    if today_date < online_price[0].price_range_end_date:
        today_range = 1
    elif today_date < online_price[1].price_range_end_date:
        today_range = 2
    else:
        today_range = 3

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
        'today_range': today_range,

    }
    return HttpResponse(template.render(context, request))
