from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

def index(request):
    '''Docstring testc'''
    template = loader.get_template('new-design/index.html')
    context = {
        'articles': range(5),
    }

    return HttpResponse(template.render(context, request))

def blog(request):
    '''Docstring testc'''
    template = loader.get_template('new-design/blog.html')
    context = {
        'articles': range(15),
    }

    return HttpResponse(template.render(context, request))

def events(request):
    '''Docstring testc'''
    template = loader.get_template('new-design/events.html')
    context = {
        'articles': range(5),
    }

    return HttpResponse(template.render(context, request))

def single_post(request):
    '''Docstring testc'''
    template = loader.get_template('new-design/single_post.html')
    context = {}

    return HttpResponse(template.render(context, request))
