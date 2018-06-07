from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def index(request):
	template = loader.get_template('mainpage/index.html')
	context = {'number': 5}
	return HttpResponse(template.render(context, request))

