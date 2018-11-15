```sh
(learnpython) denis@joy:~/p/learnpython/landing_page$ python manage.py runserver
Performing system checks...

System check identified no issues (0 silenced).
October 11, 2018 - 00:58:09
Django version 2.0.5, using settings 'landing_page.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

```txt
Received the `<WSGIRequest: POST '/timepad_ticket_status_webhook'>` request
```

```json
{
    "id": "22398681:72953815",
    "event_id": 830329,
    "organization_id": 143309,
    "order_id": "17862119",
    "reg_date": "2018-10-11 00:58:30",
    "reg_id": 1993954,
    "status": "\u0431\u0435\u0441\u043f\u043b\u0430\u0442\u043d\u043e",
    "status_raw": "ok",
    "email": "denistrofimov@pythonmachinelearningcv.com",
    "surname": "qrqr",
    "name": "qwewqe",
    "attended": false,
    "code": "72953815",
    "barcode": "1000729538159",
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
            "value": "qrqr"
        },
        {
            "id": 3518731,
            "type": "text",
            "name": "\u0418\u043c\u044f",
            "mandatory": null,
            "value": "qwewqe"
        }
    ],
    "aux": {
        "use_ticket_remind": "1"
    },
    "org_name": "PythonMachineLearningCV",
    "event_name": "\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435",
    "event_city": "\u0411\u0435\u0437 \u0433\u043e\u0440\u043e\u0434\u0430",
    "event_place": "",
    "hook_generated_at": "2018-10-11 00:58:30",
    "hook_guid": "e3cd846c-291d-494f-993a-42484b75b2f8"
}
```

```txt
[11/Oct/2018 00:58:31] "POST /timepad_ticket_status_webhook HTTP/1.1" 200 16
```

Received the <WSGIRequest: POST '/timepad_ticket_status_webhook'> request
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
    "surname": "denistrofimov",
    "name": "denistrofimov",
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

[11/Oct/2018 01:45:57] "POST /timepad_ticket_status_webhook HTTP/1.1" 200 16
Performing system checks...

System check identified no issues (0 silenced).

$ python manage.py test
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.[{'email': 'denistrofimov@pythonmachinelearningcv.com', 'status': 'sent', '_id': 'f0d5302b4aab4b5c84d14891af611c15', 'reject_reason': None}]
.
----------------------------------------------------------------------
Ran 2 tests in 1.864s

OK
Destroying test database for alias 'default'...

October 11, 2018 - 01:52:51
Django version 2.0.5, using settings 'landing_page.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
{
    "id": "22398638:25860610",
    "event_id": 830329,
    "organization_id": 143309,
    "order_id": "17862081",
    "reg_date": "2018-10-11 00:54:05",
    "reg_id": 1993954,
    "status": "\u0431\u0435\u0441\u043f\u043b\u0430\u0442\u043d\u043e",
    "status_raw": "ok",
    "email": "denistrofimov@pythonmachinelearningcv.com",
    "surname": "wert",
    "name": "wert",
    "attended": false,
    "code": "25860610",
    "barcode": "1000258606107",
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
            "value": "wert"
        },
        {
            "id": 3518731,
            "type": "text",
            "name": "\u0418\u043c\u044f",
            "mandatory": null,
            "value": "wert"
        }
    ],
    "aux": {
        "use_ticket_remind": "1"
    },
    "org_name": "PythonMachineLearningCV",
    "event_name": "\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435",
    "event_city": "\u0411\u0435\u0437 \u0433\u043e\u0440\u043e\u0434\u0430",
    "event_place": "",
    "hook_generated_at": "2018-10-11 00:54:06",
    "hook_guid": "fc9ed116-9b13-44b1-8974-7c681ca6d03b",
    "hook_resend": 2
}
[11/Oct/2018 01:54:08] "POST /timepad_ticket_status_webhook HTTP/1.1" 200 16
