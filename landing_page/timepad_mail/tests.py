import json
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

    def test_send_mail(self):
        """ Test for send a new transactional message through Mandrill using 
            real timepad webhook json data.
        """
        timepad_json_payload = """
        {
            "id": "22398586:56559903",
            "event_id": 830329,
            "organization_id": 143309,
            "order_id": "17862035",
            "reg_date": "2018-10-11 00:45:53",
            "reg_id": 1993954,
            "status": "\u0431\u0435\u0441\u043f\u043b\u0430\u0442\u043d\u043e",
            "status_raw": "ok",
            "email": "denistrofimov@pythonmachinelearningcv.com",
            "surname": "trofimov",
            "name": "denis",
            "attended": false,
            "code": "56559903",
            "barcode": "1000565599031",
            "price_nominal": "0",
            "answers": [
                {
                    "id": 3518729,
                    "type": "text",
                    "name": "E-mail",
                    "mandatory": null,
                    "value": "denistrofimov@pythonmachinelearningcv.com"
                },
                {
                    "id": 3518730,
                    "type": "text",
                    "name": "\u0424\u0430\u043c\u0438\u043b\u0438\u044f",
                    "mandatory": null,
                    "value": "denistrofimov"
                },
                {
                    "id": 3518731,
                    "type": "text",
                    "name": "\u0418\u043c\u044f",
                    "mandatory": null,
                    "value": "denistrofimov"
                }
            ],
            "aux": {
                "use_ticket_remind": "1"
            },
            "org_name": "PythonMachineLearningCV",
            "event_name": "\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435",
            "event_city": "\u0411\u0435\u0437 \u0433\u043e\u0440\u043e\u0434\u0430",
            "event_place": "",
            "hook_generated_at": "2018-10-11 00:45:54",
            "hook_guid": "710f9dbf-419b-409d-8b33-c265e6b0173d",
            "hook_resend": 2
        }
        """
        payload = json.loads(timepad_json_payload)
        responce = send_mail(payload)
        print(responce)
        self.assertEqual(responce[0]['status'], 'sent')
