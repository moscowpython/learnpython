"""Send timepad ticket status to mail."""
import mandrill

from django.conf import settings

def _create_template(payload):
    """ Create HTML with sutable data from payload."""

    cells = ''
    for key, value in payload.items():
        if key not in ("answers", "aux"):
            cells += f'<tr><td>{key}</td><td>{value}</td></tr>'

#    html = open("basic_template.html", 'rt').readlines()
    base = f"""
    <!doctype html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width" />
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    </head>
    <body>
        <table role="presentation" border="0" cellpadding="0" cellspacing="0" class="body">
        {cells}
        </table>
    </body>
    </html>
    """
    return base

def send_mail(payload):
    html = _create_template(payload)
    """ Send a new transactional message through Mandrill."""
    try:
        mandrill_client = mandrill.Mandrill(settings.MANDRILL_API_KEY)
        message = {
                   'html': html,
                   'tags': [payload['status']],
                   'to': [{'email': payload['email'],
                           'name': f"{payload['name']} {payload['surname']}",
                           'type': 'to'}],
        }
        result = mandrill_client.messages.send(
            message=message, async=False, ip_pool='Main Pool',
            send_at='example send_at'
        )
        '''
        [{'_id': 'abc123abc123abc123abc123abc123',
        'email': payload['email'],
        'reject_reason': 'hard-bounce',
        'status': 'sent'}]
        '''
        return result
    except mandrill.Error as e:
        # Mandrill errors are thrown as exceptions
        print('A mandrill error occurred: %s - %s' % (e.__class__, e))
        # A mandrill error occurred: <class 'mandrill.UnknownSubaccountError'> - No subaccount exists with the id 'customer-123'
        raise

