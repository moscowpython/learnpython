"""Timepad ticket status mailing."""
from __future__ import absolute_import, unicode_literals
from celery import shared_task
import json
import logging
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.core.exceptions import (
    ObjectDoesNotExist,
    MultipleObjectsReturned,
    ValidationError,
)
from .senders import send_template



# Get an instance of a logger
logger = logging.getLogger(__name__)

class TicketQuerySet(models.QuerySet):
    """ Ticket methods.
    
        What matters, is that implementing the methods on querysets/managers
        rather than Models would allow for more efficient queries.
        https://sunscrapers.com/blog/where-to-put-business-logic-django/
    """

    def get_ticket(self, ticket):
        "Get ticket instance."
        try:
            return self.get(order_id=ticket.order_id, event_id=ticket.event_id)
        except ObjectDoesNotExist as exception:
            logger.error(f'{exception.__class__.__name__} occurred: {exception}')
            return
        except MultipleObjectsReturned as exception:
            logger.error(f'{exception.__class__.__name__} occurred: {exception}')
            tickets = self.filter(order_id=ticket.order_id, event_id=ticket.event_id)
            return tickets[0]

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
    
    def save_ticket(self, ticket):
        "Save (store) ticket and send template email."
        ticket.save()
        response = send_template(
            template_name=ticket.status_to_template(ticket.status),
            email=ticket.email,
            surname=ticket.surname,
            name=ticket.name,
        )
        return response

    def update_ticket_status(self, ticket):
        "Update ticket status and send template email."
        try:
            read_ticket = self.get(order_id=ticket.order_id, event_id=ticket.event_id)
            read_ticket.status = ticket.status
            read_ticket.save(update_fields=('status', ))
        except ObjectDoesNotExist as exception:
            logger.error(f'{exception.__class__.__name__} occurred: {exception}')
            ticket.save()
        except MultipleObjectsReturned as exception:
            logger.error(f'{exception.__class__.__name__} occurred: {exception}')
            tickets = self.filter(order_id=ticket.order_id, event_id=ticket.event_id)
            tickets.update(status=ticket.status)
        response = send_template(
            template_name=ticket.status_to_template(ticket.status),
            email=ticket.email,
            surname=ticket.surname,
            name=ticket.name,
        )
        return response

    def update_tickets_status(self, tickets, status):
        "Update tickets status and send template emails."
        responses = []
        for ticket in tickets:
            current_tz = timezone.get_current_timezone()
            expire_date = current_tz.normalize(
                ticket.reg_date + timezone.timedelta(hours=80)
            )
            vars = [
                {
                    "name": "ddate",
                    "content": expire_date.strftime('%d.%m.%Y')
                },
                {
                    "name": "dtime",
                    "content": expire_date.strftime('%H:%M')
                },
            ]
            response = send_template(
                template_name=ticket.status_to_template(status),
                email=ticket.email,
                surname=ticket.surname,
                name=ticket.name,
                vars=vars,
            )
            responses.append(response)
            if (
                isinstance(response, list) 
                and len(response) 
                and response[0].get('status') in ('sent', 'queued')
            ):
                ticket.status = status
                ticket.save(update_fields=('status', ))
        return responses

    def send_ticket_reminder_one(self):
        """ Check expired ticket and send reminder one. 
            ticket-expiration1: 
            следующий день в 9 утра по МСК, если билет не оплачен
        """
        reminder_date = timezone.now() - timezone.timedelta(days=1)
        expire_date = timezone.now() - timezone.timedelta(days=2)
        status = Ticket.STATUS_REMINDED_1
        tickets = self.filter(
            status=Ticket.STATUS_NEW,
            reg_date__lt=reminder_date,
        ) & self.filter(
            status=Ticket.STATUS_NEW,
            reg_date__gt=expire_date,
        )    
        return Ticket.objects.update_tickets_status(tickets, status)

    def send_ticket_reminder_two(self):
        """ Check expired ticket and send reminder one. 
            ticket-expiration2
            через два дня в 9 утра по МСК, если билет не оплачен
        """
        reminder_date = timezone.now() - timezone.timedelta(days=2)
        expire_date = timezone.now() - timezone.timedelta(hours=66)
        status = Ticket.STATUS_REMINDED_2
        tickets = self.filter(
            status__in=(
                Ticket.STATUS_NEW,
                Ticket.STATUS_REMINDED_1,
            ), 
            reg_date__lt=reminder_date,
        ) & self.filter(
            status__in=(
                Ticket.STATUS_NEW,
                Ticket.STATUS_REMINDED_1,
            ), 
            reg_date__gt=expire_date,
        )  
        return Ticket.objects.update_tickets_status(tickets, status)
        
    def send_ticket_reminder_three(self):
        """ Check expired ticket and send reminder one. 

            На TimePad установлен срок брони – 80 часов. 
            Условие проверки №3: за 14 часов до конца брони, если билет
            не оплачен, означает, что билет создан ранее на 66 часов,
            чем время сейчас, на момент проверки.
        """
        reminder_date = timezone.now() - timezone.timedelta(hours=66)
        expire_date = timezone.now() - timezone.timedelta(hours=80)
        status = Ticket.STATUS_REMINDED_3
        tickets = self.filter(
            status__in=(
                Ticket.STATUS_NEW,
                Ticket.STATUS_REMINDED_1,
                Ticket.STATUS_REMINDED_2,
            ), 
            reg_date__lt=reminder_date,
        ) & self.filter(
            status__in=(
                Ticket.STATUS_NEW,
                Ticket.STATUS_REMINDED_1,
                Ticket.STATUS_REMINDED_2,
            ), 
            reg_date__gt=expire_date,
        )    
        return Ticket.objects.update_tickets_status(tickets, status)

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
        'ok': STATUS_PAID,
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
        return (f"{self.event_name}, ID заказа: {self.order_id}, "
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
        except (KeyError, ValueError) as exception:
            logger.error(f'Deserialize {exception.__class__.__name__}: '
            f'{exception}')
            return
        except ValidationError as exception:
            logger.error(f'Deserialize {exception.__class__.__name__}: '
            f'{exception}')
            logger.error(f'Invalid ticket: {ticket}')
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
                return ticket, cls.objects.save_ticket(ticket)
            elif ticket:
                return ticket, cls.objects.update_ticket_status(ticket)
            return ticket
