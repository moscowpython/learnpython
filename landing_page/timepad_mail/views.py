import hashlib
import hmac
import json

from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt


def process_webhook(payload):
    """Simple webhook handler that prints the event and payload to the console"""
    print(json.dumps(payload, indent=4))


@csrf_exempt
def handle_webhook(request):
    """Webhook handler check sender sha1 signature."""
    # TODO: wrap in try-except, use safe get, etc.
    # Check the X-Hub-Signature header to make sure this is a valid request.
    message_signature = request.META['HTTP_X_HUB_SIGNATURE']
    # Solution: hmac works with ``bytes``, not ``str``.
    key_bytes = bytes(settings.TIMEPAD_WEBHOOK_SECRET , 'utf8')
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
