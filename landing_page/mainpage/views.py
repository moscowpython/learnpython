from datetime import date

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from waffle import switch_is_active

from .models import CourseReview, Curators, Enrollment, EnrollmentType, GraduateProjects


def index(request: HttpRequest) -> HttpResponse:
    enrollment = Enrollment.get_enrollment_with_active_registration(enrollment_type=EnrollmentType.BASE)
    context = {
        'enrollment': enrollment,
        'projects': GraduateProjects.objects.all(),
        'registration_closes_date_formatted': (
            enrollment.end_registration_date.strftime('%b %d, %Y %H:%M:%S')
            if enrollment else ""
        ),
        'curators_list': Curators.objects.filter(is_visible=True),
        'today': date.today(),
        'reviews': CourseReview.objects.filter(review_for=EnrollmentType.BASE),
        'should_show_chat': switch_is_active('show_tg_chat_widget'),
    }
    return render(request, 'mainpage/index.html', context)


def advanced_handle(request: HttpRequest) -> HttpResponse:
    enrollment = Enrollment.get_enrollment_with_active_registration(enrollment_type=EnrollmentType.ADVANCED)
    return render(
        request,
        'mainpage/advanced.html',
        context={
            'today': date.today(),
            'enrollment': enrollment,
            'registration_closes_date_formatted': (
                enrollment.end_registration_date.strftime('%b %d, %Y %H:%M:%S')
                if enrollment else ""
            ),
        },
    )


def success_handle(request: HttpRequest) -> HttpResponse:
    enrollment = Enrollment.get_enrollment_with_active_registration(enrollment_type=EnrollmentType.BASE)
    return render(
        request,
        'mainpage/success.html',
        context={
            'enrollment': enrollment,
        },
    )


def success_handle_advanced(request: HttpRequest) -> HttpResponse:
    enrollment = Enrollment.get_enrollment_with_active_registration(enrollment_type=EnrollmentType.ADVANCED)
    return render(
        request,
        'mainpage/success.html',
        context={
            'enrollment': enrollment,
        },
    )
