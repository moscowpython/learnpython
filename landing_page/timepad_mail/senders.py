# -*- coding: UTF-8 -*-
"""Send timepad ticket status to mail."""
import logging
import mandrill
from django.utils import timezone
from django.conf import settings


# Get an instance of a logger
logger = logging.getLogger(__name__)

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
    send_at = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        mandrill_client = mandrill.Mandrill(settings.MANDRILL_API_KEY)     
        result = mandrill_client.messages.send(
            message=message, async=False, send_at=send_at
        )
        return result
    except mandrill.Error as e:
        # Mandrill errors are thrown as exceptions
        print('A mandrill {0} occurred: {1}'.format(e.__class__.__name__, e))
        raise

def send_template(*, template_name, email, name, surname, vars=[]):
    """ Send a new transactional message through Mandrill using a template.

        Example Call fixed syntax for Python 3
        https://mandrillapp.com/api/docs/messages.python.html#method=send-template

        :param template_name: the name or slug of a template in the user's account
        :param email: email
        :param name: name
        :param surname: surname or family name
        :param vars: merge tags JSON, 
        paylink - ссылка на страницу оплаты заказа в таймпад
        ddate - дата истечения брони (формат дд.мм.гггг)
        dtime - время истечения брони (формат чч:мм)
        maximum example from KK:
        [
            {
                "name": "paylink",
                "content": "http://example"
            },
            {
                "name": "ddate",
                "content": "22.12.1234"
            },
            {
                "name": "dtime",
                "content": "12:12"
            }
        ]
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
    message = {
        "merge_vars": [
            {
                "rcpt": email,
                "vars": vars
            },
        ],
        'subject': 'Набор на курсы Learn Python.',
        'from_email': 'learn@python.ru',
        'from_name': 'Learn Python Team',
        'to': [
            {
                'email': email,
                'name': f"{name} {surname}",
                'type': 'to'
            }
        ],
        'important': True,
        'tags': [template_name],
    }
    """send_at: string when this message should be sent 
    as a UTC timestamp in YYYY-MM-DD HH:MM:SS format."""
    send_at = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        mandrill_client = mandrill.Mandrill(settings.MANDRILL_API_KEY)
        result = mandrill_client.messages.send_template(
            template_name=template_name, 
            template_content=(), 
            message=message, 
            async=False, 
            send_at=send_at,
        )
        status = result[0]['status']
        
        if status in ('sent', 'queued'):
            logger.info(f'{send_at} - {template_name} is {status} for '
            f'{email}')
        else:
            logger.error(f'{send_at} - {template_name} is {status} for '
            f'{email}')
            logger.debug(f'{send_at} - Mandrill Response JSON: {result}')
        return result
    except mandrill.Error as exception:
        # Mandrill errors are thrown as exceptions
        logger.error(f'{send_at} - A Mandrill {exception.__class__.__name__}'
        f' occurred: {exception}')
