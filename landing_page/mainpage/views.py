from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import MoscowPythonMeetup, LearnPythonCourse, GraduateProjects


def index(request):
	template = loader.get_template('mainpage/index.html')
	current_meetup = MoscowPythonMeetup.objects.latest('meetup_number')
	current_course = LearnPythonCourse.objects.latest('course_index')
	student_projects = list(GraduateProjects.objects.all())

	context = {
		'meetup': current_meetup,
		'course': current_course,
		'projects': student_projects
	}
	return HttpResponse(template.render(context, request))

