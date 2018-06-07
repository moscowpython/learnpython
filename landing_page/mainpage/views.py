from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import MoscowPythonMeetup


def index(request):
	template = loader.get_template('mainpage/index.html')
	current_meetup = MoscowPythonMeetup.objects.latest('meetup_number')
	context = {
		'meetup': current_meetup
	}
	return HttpResponse(template.render(context, request))

