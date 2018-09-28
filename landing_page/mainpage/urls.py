from django.urls import path
from django.http import HttpResponse

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('robots.txt', lambda x: HttpResponse('User-agent: *\nDisallow: *lessons*\nHost: https://learn.python.ru/', content_type="text/plain")),
]
