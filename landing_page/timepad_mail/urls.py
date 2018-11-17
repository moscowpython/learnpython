from django.urls import include, path
from . import views

# Django integration with RQ, a Redis based Python queuing library.
# For Django >= 2.0
urlpatterns = [
    path('timepad_ticket_status_webhook',
        views.handle_webhook,
        'ticket_status_webhook',
        {'kind': 'ticket'},
    ),
    path('timepad_order_status_webhook',
        views.handle_webhook,
        'order_status_webhook',
        {'kind': 'order'},
    ),
]
