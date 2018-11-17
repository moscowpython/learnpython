import hashlib
import hmac
import json

from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from .tasks import process_webhook_payload, process_order_payload


@csrf_exempt
def handle_webhook(request, **kwargs):
    """Webhook handler check sender sha1 signature."""
    # TODO: wrap in try-except, use safe get, etc.
    # Check the X-Hub-Signature header to make sure this is a valid request.
    if not 'HTTP_X_HUB_SIGNATURE' in request.META:
        return HttpResponseForbidden('Invalid signature header')
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
        payload = request.POST['payload']
    else:
        payload = request.body

    """ Workaround of issue #10.
        Calling process_webhook_async.delay(payload): 
        Object of type 'bytes' is not JSON serializable.
    """
    if isinstance(payload, bytes):
        # 'ignore' (just leave the character out of the Unicode result)
        payload = payload.decode("utf-8", "ignore")

    # This is where you'll do something with the webhook
    if kwargs['kind'] == 'ticket':
        process_webhook_payload(payload)
    elif kwargs['kind'] == 'order':
        process_order_payload(payload)

    return HttpResponse('Webhook received', status=200)
