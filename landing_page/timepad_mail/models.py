"""Timepad ticket status mailing."""
from django.db import models
from django.utils import timezone


class Ticket(models.Model):
    """ Ticket from the timepad.

    Содержание JSON запроса для хука изменения статусов билетов #
    {
    "id": "5184211:83845994", // ID билета (печататется на самом билете)
    "event_id": 215813, // ID мероприятия
    "organization_id": 29963, // ID организации, создавшей мероприятие
    "order_id": "4955686", // ID заказа
    "reg_date": "2015-07-24 19:04:37", // Дата заказа билета
    "reg_id": 361138, // Внутренний ID билета
    "status": "забронировано", // Статус заказа / билета
    "status_raw": "booked", // Статус заказа в машиночитаемом формате
    "email": "test-mail@ya.ru", // E-mail заказчика
    "surname": "Смирнов", // Фамилия на билете
    "name": "Владимир", // Имя на билете
    "attended": false, // Отметка о посещении мероприятия
    "code": "83845994", // Числовой код билета
    "barcode": "1000838459949", // Числовой код в формате EAN-13, напечатан на билете в виде штрих-кода
    "price_nominal": 1000, // Стоимость билета на момент заказа 
    "answers": [ // Список ответов на вопросы анкеты (если есть)
        {
        "id": 889802, // ID вопроса
        "type": "text", // Тип вопроса
        "name": "E-mail", // Текст вопроса
        "mandatory": null, // Обязательность вопроса
        "value": "test-mail@ya.ru" // Текст ответа
        },
        {
        "id": 889803, // ID вопроса
        "type": "text", // Тип вопроса
        "name": "Фамилия", // Текст вопроса
        "mandatory": null, // Обязательность вопроса
        "value": "Смирнов" // Текст ответа
        },
        {
        "id": 889804, // ID вопроса
        "type": "text", // Тип вопроса
        "name": "Имя", // Текст вопроса
        "mandatory": null, // Обязательность вопроса
        "value": "Владимир" // Текст ответа
        }
    ],
    "aux": []
    }
    """
    STATUS_PAID = 'p'
    STATUS_CANCELED = 'c'
    STATUS_NEW = 'n'
    STATUS_REMINEDED_1 ='1'
    STATUS_REMINEDED_2 ='2'
    STATUS_REMINEDED_3 ='3'
    STATUS_CHOICES = (
        (STATUS_NEW, 'новый'),
        (STATUS_PAID, 'оплачено'),
        (STATUS_CANCELED, 'отказ'),
        (STATUS_REMINEDED_1, 'напоминание 1'),
        (STATUS_REMINEDED_2, 'напоминание 2'),
        (STATUS_REMINEDED_3, 'напоминание 3'),
    )
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
    order_id = models.IntegerField('ID заказа')
    ticket_id = models.CharField(
        'ID',
        max_length=20,
    )
    code = models.IntegerField('код')
    barcode = models.BigIntegerField('штрих-код')
    email = models.EmailField('e-mail')
    name = models.CharField(
        'имя',
        max_length=20,
    )
    surname = models.CharField(
        'фамилия',
        max_length=64,
    )    
    """ Статус заказа в машиночитаемом формате."""
    status_raw = models.CharField(
        'статус',
        max_length=1,
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
        blank=False,
    )
    """ "2015-07-24 19:04:37", Дата заказа билета"""
    reg_date = models.DateTimeField('дата заказа')
    reg_id = models.BigIntegerField('внутренний ID')

    class Meta:
        verbose_name = 'билет'
        verbose_name_plural = 'билеты'

    def __str__(self):
        return 'Билет {0}, статус {1}'.format(self.ticket_id, self.status_raw)
        