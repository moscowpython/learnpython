from django.urls import path

from . import (
    views,
    views_new_design,
)

urlpatterns = [
    path('', views.index, name='index'),
    path('projects', views.projects, name='projects'),
    path('new', views_new_design.index, name='new-index'),
    path('new/blog', views_new_design.blog, name='new-blog'),
    path('new/events', views_new_design.events, name='new-events'),
    path('new/single_post', views_new_design.single_post, name='new-single_post'),
]
