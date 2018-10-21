from django.test import TestCase, SimpleTestCase

from .send_mail_mandrill import send_mail, _create_html_table_from_dict


class MandrillSendTest(SimpleTestCase):
    

    def test_create_html_table_from_dict(self):
        """ Create HTML with sutable data from payload."""
        payload = {"event_id": 830329, "order_id": "17862035"}
        html = _create_html_table_from_dict(payload)
        self.assertInHTML("event_id", html)
        self.assertInHTML("830329", html)
        self.assertInHTML("order_id", html)
        self.assertInHTML("17862035", html)