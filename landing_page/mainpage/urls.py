from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('success/', views.success_handle, name='success'),

    path('advanced/', views.advanced_handle, name='index_advanced'),
    path('advanced/success/', views.success_handle_advanced, name='success_advanced'),

]
