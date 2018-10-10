"""landing_page URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from timepad_mail import views

urlpatterns = [
    path('', include('mainpage.urls')),
    path('admin/', admin.site.urls),
]

# Django integration with RQ, a Redis based Python queuing library.
# For Django >= 2.0
urlpatterns += [
    path('django-rq/', include('django_rq.urls')),
    path('timepad_ticket_status_webhook', views.handle_webhook, name='webhook'),
]
