from django.urls import include, path
from . import views

# Django integration with RQ, a Redis based Python queuing library.
# For Django >= 2.0
urlpatterns = [
    path('timepad_ticket_status_webhook',
        views.handle_webhook,
        name='ticket_status_webhook'),
]
