from django.urls import path
from django.views.generic.simple import direct_to_template

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    (r'^robots\.txt$', direct_to_template,
     {'template': 'robots.txt', 'mimetype': 'text/plain'})
]
