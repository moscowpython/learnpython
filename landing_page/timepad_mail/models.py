"""Timepad ticket status mailing."""
from __future__ import absolute_import, unicode_literals
from celery import shared_task
import json
import logging
from django.db import models
from django.utils import timezone
from django.core.exceptions import (
    ObjectDoesNotExist,
    MultipleObjectsReturned,
    ValidationError,
)
from .send_mail_mandrill import send_template



# Get an instance of a logger
logger = logging.getLogger(__name__)

class TicketQuerySet(models.QuerySet):
    """ Ticket methods.
    
        What matters, is that implementing the methods on querysets/managers
        rather than Models would allow for more efficient queries.
        https://sunscrapers.com/blog/where-to-put-business-logic-django/
    """

    # def create_ticket(self, **kwargs):
    #     " Create ticket instance."
    #     return self.create(**kwargs)

    def create_ticket(self, **kwargs):
        """ Ticket create customization that send mail.

            :return: new Ticket 
        """
        ticket = self.create(**kwargs)
        send_template(
            template_name=ticket.status_to_template(ticket.status),
            email=ticket.email,
            surname=ticket.surname,
            name=ticket.name,
        )
        return ticket
    
    # @shared_task
    def save_ticket(self, ticket):
        ticket.save()
        send_template(
            template_name=ticket.status_to_template(ticket.status),
            email=ticket.email,
            surname=ticket.surname,
            name=ticket.name,
        )
        return ticket

    def update_ticket_status(self, ticket):
        "Update ticket status."
        tickets = self.filter(order_id=ticket.order_id, event_id=ticket.event_id)
        for old_ticket in tickets:
            send_template(
                template_name=ticket.status_to_template(ticket.status),
                email=ticket.email,
                surname=ticket.surname,
                name=ticket.name,
            )
        tickets.update(status=ticket.status)

class Ticket(models.Model):
    """ Ticket from the timepad.

        :param event_id: 215813, ID мероприятия
        :param order_id: "4955686", ID заказа
        :param reg_date: "2015-07-24 19:04:37", Дата заказа билета
        :param status: Статус заказа в машиночитаемом формате
        :param email: "test-mail@ya.ru", E-mail заказчика
        :param surname: "Смирнов", Фамилия на билете
        :param name: "Владимир", Имя на билете
        :param printed_id: "5184211:83845994", ID билета печататется
        :param event_name: название
    """
    CAMPAIGN_EVENTS = ('Learn Python 11', )
    STATUS_PAID = 'p'
    STATUS_CANCELED = 'c'
    STATUS_NEW = 'n'
    STATUS_REMINDED_1 ='1'
    STATUS_REMINDED_2 ='2'
    STATUS_REMINDED_3 ='3'
    STATUS_CHOICES = (
        (STATUS_NEW, 'новый'),
        (STATUS_PAID, 'оплачено'),
        (STATUS_CANCELED, 'отказ'),
        (STATUS_REMINDED_1, 'напоминание 1'),
        (STATUS_REMINDED_2, 'напоминание 2'),
        (STATUS_REMINDED_3, 'напоминание 3'),
    )
    STATUS_TEMPLATE = {
        STATUS_PAID: 'ticket-success',
        STATUS_CANCELED: 'ticket-cancel',
        STATUS_NEW: 'ticket-creation',
        STATUS_REMINDED_1: "ticket-expiration1",
        STATUS_REMINDED_2: "ticket-expiration2",
        STATUS_REMINDED_3: "ticket-expiration3",
    }
    
    """ Status to action required correspondance.
        paid (оплачено): платный билет успешно оплачен он-лайн
        booked (забронировано): билет находится в статусе "Забронировано"
        notpaid (просрочено): билет не был оплачен и срок брони для него истек
        inactive (отказ): участник отказался от участия
        booked_offline (бронь для выкупа): билет был заказан для выкупа в офисе 
        организатора
        paid_offline (оплачено на месте): билет был оплачен в офисе организатора
        paid_ur (оплачено компанией): билет был оплачен юридическим платежом
        transfer_payment (перенесена оплата): билет был оплачен переносом оплаты 
        с другого заказа
    """
    STATUS_RAW_TO_CHOICE = {
        'paid': STATUS_PAID,
        'paid_ur': STATUS_PAID,
        'paid_offline': STATUS_PAID,
        'transfer_payment': STATUS_PAID,
        'inactive': STATUS_CANCELED,
        'notpaid': STATUS_CANCELED,
        'booked': STATUS_NEW,
        'booked_offline': STATUS_NEW,
    }
    order_id = models.IntegerField('ID заказа')
    event_id = models.IntegerField('ID мероприятия')
    """ Статус заказа в машиночитаемом формате."""
    status = models.CharField(
        'статус',
        max_length=1,
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
        blank=False,
    )
    """ "2015-07-24 19:04:37", Дата заказа билета"""
    reg_date = models.DateTimeField('дата заказа')
    email = models.EmailField('e-mail')
    name = models.CharField(
        'имя',
        max_length=20,
    )
    surname = models.CharField(
        'фамилия',
        max_length=32,
    )    
    printed_id = models.CharField(
        'ID печатный',
        max_length=20,
    )
    event_name = models.CharField(
        'событие',
        max_length=32,
    ) 
    """ The reason why I’m saying queryset/managers is that in Django
        you can easily get one from the other, e.g. defining a queryset
        but then calling the as_manager().
    """
    objects = TicketQuerySet.as_manager()
    # code = models.IntegerField('код')
    # barcode = models.BigIntegerField('штрих-код')
    # reg_id = models.BigIntegerField('внутренний ID')

    class Meta:
        verbose_name = 'билет'
        verbose_name_plural = 'билеты'
        # unique_together = (('order_id', 'event_id',),)
        indexes = [
            models.Index(
                fields=['order_id', 'event_id',], 
                name='unique_ticket_index'
            ),
            models.Index(
                fields=['status', 'reg_date',],
                name='expiration_ticket_index' 
            ),
        ]

    def __str__(self):
        return (f"ID билета: {self.printed_id}, ID заказа: {self.order_id}, "
        f"ID мероприятия: {self.event_id}, Дата: {self.reg_date}, "
        f"Статус: {self.status}, E-mail: {self.email}, "
        f"Имя: {self.name}, Фамилия: {self.surname}")

    def __repr__(self):
        return f"""
            ==================билет=====================
            {self.id}: ID билета в БД
            {self.printed_id}: ID билета (печататется на самом билете)
            {self.event_id}: ID мероприятия
            {self.order_id}: ID заказа
            {self.reg_date}: Дата заказа билета
            {self.status}: Статус заказа в машиночитаемом формате
            {self.email}: E-mail заказчика
            {self.surname}: Фамилия на билете
            {self.name}: Имя на билете
            ============================================
            """

    @classmethod
    def get_status_from_raw(cls, status_raw: str) -> str:
        " Convert status_raw to constant statuses, None on fail."
        status = cls.STATUS_RAW_TO_CHOICE.get(status_raw)
        return status

    @staticmethod
    def reg_date_to_datatime(reg_date: str) -> timezone.datetime:
        """ Convert status_raw to constant statuses, None on fail.
            :param reg_date: "2015-07-24 19:04:37", // Дата заказа билета
            :return: timezone.datetime reg_date
        """
        try:
            naive_datetime = timezone.datetime.strptime(
                reg_date, '%Y-%m-%d %H:%M:%S'
            )
            current_tz = timezone.get_current_timezone()
            return current_tz.localize(naive_datetime) 
        except BaseException as e:
            logger.error(e)

    @classmethod
    def status_to_template(cls, status: str) -> str:
        " Convert status to template_name, None on fail."
        return cls.STATUS_TEMPLATE.get(status)

    @classmethod
    def dict_deserialize(cls, data: dict):
        """ Deserialize a ticket from a Timepad JSON parsed to dict.
        
            :param data: a Timepad payload JSON parsed to dict.
            :return: a Ticket instance or None on error.
        """
        try:
            ticket = cls(
                order_id=int(data['order_id']),
                event_id=int(data['event_id']), 
                status=cls.get_status_from_raw(data['status_raw']), 
                reg_date=cls.reg_date_to_datatime(data['reg_date']),
                email=data['email'],
                name=data['name'],
                surname=data['surname'],
                printed_id=data['id'],
                event_name=data['event_name'],
            )
            ticket.full_clean()
            return ticket
        except (KeyError, ValueError, ValidationError) as e:
            logger.error(e)
            return

    @classmethod
    def manage_webhook_payload(cls, payload: str):
        try:
            payload_dict = json.loads(payload)
        except json.JSONDecodeError as e:
            logger.error(e)
            return
        status = cls.get_status_from_raw(payload_dict['status_raw'])
        event_name = payload_dict['event_name']
        

        if not status:
            logger.info(f"{payload_dict['status_raw']} is not targeted.")
        elif not event_name in cls.CAMPAIGN_EVENTS:
            """ If an event is not in campaign, no action required."""
            logger.info(f"{event_name} is not in campaign, no action required.")
        else:
            ticket = cls.dict_deserialize(payload_dict)
            if ticket and ticket.status == cls.STATUS_NEW:
                cls.objects.save_ticket(ticket)
            elif ticket:
                cls.objects.update_ticket_status(ticket)
            return ticket
