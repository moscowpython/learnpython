# -*- coding: UTF-8 -*-
"""Send timepad ticket status to mail."""
from datetime import datetime
import mandrill

# from django.utils import timezone
from django.conf import settings

def _create_html_table_from_dict(payload: dict) -> str:
    """ Create HTML with sutable data from payload."""
#    html = open("basic_template.html", 'rt').readlines()
    cells = ''
    for key, value in payload.items():
        if key not in ("answers", "aux"):
            cells += f'<tr><td>{key}</td><td>{value}</td></tr>'
    base = f"""
    <!doctype html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width" />
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    </head>
    <body>
    <table role="presentation" border="0" cellpadding="0" cellspacing="0" 
        class="body">
    {cells}
    </table>
    </body>
    </html>
    """
    return base

def send_mail(payload: dict) -> list:
    """ Send a new transactional message through Mandrill.

        Example Call fixed syntax for Python 3
        https://mandrillapp.com/api/docs/messages.python.html#method=send

        :returns: responce in JSON
        [
            {
                '_id': 'abc123abc123abc123abc123abc123',
                'email': payload['email'],
                'reject_reason': 'hard-bounce',
                'status': 'sent'
            }
        ]
    """
    html = _create_html_table_from_dict(payload)
    try:
        mandrill_client = mandrill.Mandrill(settings.MANDRILL_API_KEY)
        message = {
            'html': html,
            'subject': 'Набор на курсы Learn Python.',
            'from_email': 'learn@python.ru',
            'from_name': 'Learn Python Team',
            'to': [{'email': payload['email'],
                    'name': f"{payload['name']} {payload['surname']}",
                    'type': 'to'}],
            'important': True,

            'tags': [payload['status']],
        }
        """send_at: string when this message should be sent 
        as a UTC timestamp in YYYY-MM-DD HH:MM:SS format."""
        sent_at = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        
        result = mandrill_client.messages.send(
            message=message, async=False, send_at=sent_at
        )
        return result
    except mandrill.Error as e:
        # Mandrill errors are thrown as exceptions
        print('A mandrill error occurred: %s - %s' % (e.__class__, e))
        # A mandrill error occurred: <class 'mandrill.UnknownSubaccountError'> - No subaccount exists with the id 'customer-123'
        raise


def send_template(payload):
    """ Send a new transactional message through Mandrill using a template.

        Example Call fixed syntax for Python 3
        https://mandrillapp.com/api/docs/messages.python.html#method=send-template

        :returns: responce in JSON
        [
            {
                '_id': 'abc123abc123abc123abc123abc123',
                'email': payload['email'],
                'reject_reason': 'hard-bounce',
                'status': 'sent'
            }
        ]
    """
    try:
        mandrill_client = mandrill.Mandrill(settings.MANDRILL_API_KEY)
        template_content = [
            {'content': 'example content', 'name': 'example name'}]
        message = {'attachments': [{'content': 'ZXhhbXBsZSBmaWxl',
                                    'name': 'myfile.txt',
                                    'type': 'text/plain'}],
                   'auto_html': None,
                   'auto_text': None,
                   'bcc_address': 'message.bcc_address@example.com',
                   'from_email': 'message.from_email@example.com',
                   'from_name': 'Example Name',
                   'global_merge_vars': [{'content': 'merge1 content', 'name': 'merge1'}],
                   'google_analytics_campaign': 'message.from_email@example.com',
                   'google_analytics_domains': ['example.com'],
                   'headers': {'Reply-To': 'message.reply@example.com'},
                   'html': '<p>Example HTML content</p>',
                   'images': [{'content': 'ZXhhbXBsZSBmaWxl',
                               'name': 'IMAGECID',
                               'type': 'image/png'}],
                   'important': False,
                   'inline_css': None,
                   'merge': True,
                   'merge_language': 'mailchimp',
                   'merge_vars': [{'rcpt': payload['email'],
                                   'vars': [{'content': 'merge2 content', 'name': 'merge2'}]}],
                   'metadata': {'website': 'www.example.com'},
                   'preserve_recipients': None,
                   'recipient_metadata': [{'rcpt': payload['email'],
                                           'values': {'user_id': 123456}}],
                   'return_path_domain': None,
                   'signing_domain': None,
                   'subaccount': 'customer-123',
                   'subject': 'example subject',
                   'tags': ['password-resets'],
                   'text': 'Example text content',
                   'to': [{'email': payload['email'],
                           'name': payload['name'],
                           'type': 'to'}],
                   'track_clicks': None,
                   'track_opens': None,
                   'tracking_domain': None,
                   'url_strip_qs': None,
                   'view_content_link': None}
        result = mandrill_client.messages.send_template(
            template_name='example template_name', template_content=template_content, message=message, async=False, ip_pool='Main Pool', send_at='example send_at')
        print(result)
    except mandrill.Error as e:
        # Mandrill errors are thrown as exceptions
        print('A mandrill error occurred: %s - %s' % (e.__class__, e))
        # A mandrill error occurred: <class 'mandrill.UnknownSubaccountError'> - No subaccount exists with the id 'customer-123'
        raise
