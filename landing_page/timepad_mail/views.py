import hashlib
import hmac
import json

from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from .send_mail_mandrill import send_template, send_mail


""" Status to action required correspondance.

paid (оплачено): платный билет успешно оплачен он-лайн
booked (забронировано): билет находится в статусе "Забронировано"
notpaid (просрочено): билет не был оплачен и срок брони для него истек
inactive (отказ): участник отказался от участия
booked_offline (бронь для выкупа): билет был заказан для выкупа в офисе 
организатора
paid_offline (оплачено на месте): билет был оплачен в офисе организатора
paid_ur (оплачено компанией): билет был оплачен юридическим платежом
transfer_payment (перенесена оплата): билет был оплачен переносом оплаты 
с другого заказа
"""
STATUS_ACTION = {
    'paid': 'ticket-success',
    'paid_ur': 'ticket-success',
    'paid_offline': 'ticket-success',
    'transfer_payment': 'ticket-success',
    'inactive': 'ticket-cancel',
    'notpaid': 'ticket-cancel',
    'booked': 'ticket-creation',
    'booked_offline': 'ticket-creation',
}

def process_webhook(payload):
    """Simple webhook handler that prints the event and payload."""
    print(json.dumps(payload, indent=4))
    result = send_mail(json.loads(payload))
    print(result)

def parse_webhook_payload(payload: str):
    try:
        payload_dict = json.loads(payload)
    except json.JSONDecodeError:
        # TODO: log error
        return
    status = payload_dict.get('status_raw')
    action = STATUS_ACTION.get(status)
    if not action:
        # no action required
        return
    # TODO: queue an action


@csrf_exempt
def handle_webhook(request):
    """Webhook handler check sender sha1 signature."""
    # TODO: wrap in try-except, use safe get, etc.
    # Check the X-Hub-Signature header to make sure this is a valid request.
    message_signature = request.META['HTTP_X_HUB_SIGNATURE']
    # Solution: hmac works with ``bytes``, not ``str``.
    key_bytes = bytes(settings.TIMEPAD_WEBHOOK_SECRET, 'utf8')
    signature = hmac.new(
        key_bytes, request.body, hashlib.sha1)
    expected_signature = 'sha1=' + signature.hexdigest()
    if not hmac.compare_digest(message_signature, expected_signature):
        return HttpResponseForbidden('Invalid signature header')

    # Sometimes the payload comes in as the request body, sometimes it comes in
    # as a POST parameter. This will handle either case.
    if 'payload' in request.POST:
        payload = json.loads(request.POST['payload'])
    else:
        payload = json.loads(request.body)

    # This is where you'll do something with the webhook
    process_webhook(payload)

    return HttpResponse('Webhook received', status=200)
