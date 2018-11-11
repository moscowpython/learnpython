import json
from django.test import SimpleTestCase

from .send_mail_mandrill import (
    send_mail, _create_html_table_from_dict, send_template)


class MandrillSendTest(SimpleTestCase):
    """ Tests for send a transactional messages through Mandrill."""
    test_email = "denistrofimov@pythonmachinelearningcv.com"
    test_surname = "Трофимов"
    test_name = "Денис"

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

    def test_create_html_table_from_dict(self):
        """ Create HTML with sutable data from payload."""
        payload = {"event_id": 830329, "order_id": "17862035"}
        html = _create_html_table_from_dict(payload)
        self.assertInHTML("event_id", html)
        self.assertInHTML("830329", html)
        self.assertInHTML("order_id", html)
        self.assertInHTML("17862035", html)

    # def test_send_mail(self):
    #     """ Test for send a new transactional message through Mandrill using 
    #         real timepad webhook json data.
    #     """
    #     payload = json.loads(self.timepad_json_payload)
    #     result = send_mail(payload)
    #     print(result)
    #     self.assertEqual(result[0]['status'], 'sent')

    def __send_template_ticket_creation(self):
        """ Test for send a new message through Mandrill using a template.

            result = [
                {
                    'email': 'denistrofimov@pythonmachinelearningcv.com',
                    'status': 'sent', 
                    '_id': 'd32e79d1922a4a34ae89d7cfc27dd246', 
                    'reject_reason': None
                }
            ]
        """
        kwargs = {
            "template_name": "ticket-success",
            "email": self.test_email,
            "surname": self.test_surname,
            "name": self.test_name,
        }
        result = send_template(**kwargs)
        self.assertEqual(result[0]['status'], 'sent')
        self.assertEqual(result[0]['reject_reason'], None)
        self.assertEqual(result[0]['email'], self.test_email)
        
    def test_send_template_all_cases(self):
        """ Test for send a new message through Mandrill using a template.

            result = [
                {
                    'email': 'denistrofimov@pythonmachinelearningcv.com',
                    'status': 'sent', 
                    '_id': 'd32e79d1922a4a34ae89d7cfc27dd246', 
                    'reject_reason': None
                }
            ]
        """
        kwargs = {
            "email": self.test_email,
            "surname": self.test_surname,
            "name": self.test_name,
        }
        templates = (
            {
                "template_name": "ticket-success", 
            },
            {
                "template_name": "ticket-cancel", 
            },        
            {
                "template_name": "ticket-creation",
                'vars': [
                    {
                        "name": "paylink",
                        "content": "http://example",
                    },
                ],
            },
            {
                "template_name": "ticket-expiration1",
                'vars': [
                    {
                        "name": "paylink",
                        "content": "http://example",
                    },
                    {
                        "name": "ddate",
                        "content": "22.12.1234"
                    },
                    {
                        "name": "dtime",
                        "content": "12:12"
                    },
                ],
            },
            {
                "template_name": "ticket-expiration2",
                'vars': [
                    {
                        "name": "paylink",
                        "content": "http://example",
                    },
                    {
                        "name": "ddate",
                        "content": "22.12.1234"
                    },
                    {
                        "name": "dtime",
                        "content": "12:12"
                    },
                ],
            },   
            {
                "template_name": "ticket-expiration3",
                'vars': [
                    {
                        "name": "paylink",
                        "content": "http://example",
                    },
                    {
                        "name": "ddate",
                        "content": "22.12.1234"
                    },
                    {
                        "name": "dtime",
                        "content": "12:12"
                    },
                ],
            },                                       
        )
        for template in templates:
            for key, value in template.items():
                kwargs[key] = value
            print(kwargs["template_name"])
            result = send_template(**kwargs)
            self.assertEqual(result[0]['status'], 'sent')
            self.assertEqual(result[0]['reject_reason'], None)
            self.assertEqual(result[0]['email'], self.test_email)