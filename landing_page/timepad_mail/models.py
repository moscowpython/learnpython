"""Timepad ticket status mailing."""
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

    @staticmethod
    def get_status_from_raw(status_raw: str) -> str:
        " Convert status_raw to constant statuses, None on fail."
        status = Ticket.STATUS_RAW_TO_CHOICE.get(status_raw, None)
        if not status:
            logger.error(f'KeyError no such status as {status_raw}')
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

    @staticmethod
    def status_to_template(status: str) -> str:
        " Convert status to template_name, None on fail."
        try:
            return Ticket.STATUS_TEMPLATE.get(status, None)
        except BaseException as e:
            logger.error(e)

    @staticmethod
    def dict_deserialize(data: dict):
        """ Deserialize a ticket from a Timepad JSON parsed to dict.
        
            :param data: a Timepad payload JSON parsed to dict.
            :return: a Ticket instance or None on error.
        """
        try:
            ticket = Ticket(
                order_id=int(data['order_id']),
                event_id=int(data['event_id']), 
                status=TicketQuerySet.get_status_from_raw(data['status_raw']), 
                reg_date=TicketQuerySet.reg_date_to_datatime(data['reg_date']),
                email=data['email'],
                name=data['name'],
                surname=data['surname'],
                printed_id=data['id'],
            )
            ticket.full_clean()
            return ticket
        except (KeyError, ValueError, ValidationError) as e:
            logger.error(e)
            return

    def create_ticket(
        self, *, order_id, event_id, status, reg_date, email, name, 
        surname, printed_id, **kwargs
    ):
        """ Ticket create customization that send mail.

            :param event_id: 215813, ID мероприятия
            :param order_id: "4955686", ID заказа
            :param reg_date: "2015-07-24 19:04:37", Дата заказа билета
            :param status: Статус заказа в машиночитаемом формате
            :param email: "test-mail@ya.ru", E-mail заказчика
            :param surname: "Смирнов", Фамилия на билете
            :param name: "Владимир", Имя на билете
            :param printed_id: "5184211:83845994", ID билета 
                (печататется на самом билете)
            :return: new Ticket 
        """
        if self.filter(order_id=order_id, event_id=event_id).exists():
            # TODO: exectional situation, double webhook
            return None
        ticket = self.create(
            order_id=order_id,
            event_id=event_id, 
            status=status, 
            reg_date=reg_date,
            email=email,
            name=name,
            surname=surname,
            printed_id=printed_id,
        )
        send_template(
            template_name=self.status_to_template(ticket.status),
            email=ticket.email,
            surname=ticket.surname,
            name=ticket.name,
        )
        return ticket
    
    def create_ticket(self, ticket):
        new_ticket = self.create(
            order_id=ticket.order_id,
            event_id=ticket.event_id, 
            status=ticket.status, 
            reg_date=ticket.reg_date,
            email=ticket.email,
            name=ticket.name,
            surname=ticket.surname,
            printed_id=ticket.printed_id,
        )
        # send_template(
        #     template_name=self.status_to_template(new_ticket.status),
        #     email=new_ticket.email,
        #     surname=new_ticket.surname,
        #     name=new_ticket.name,
        # )
        return new_ticket

    def set_ticket_status(
        self, *, order_id, event_id, status, reg_date, email, name, 
        surname, printed_id, **kwargs
    ) -> int:
        """ Set ticket status to `status_raw`.

        :param event_id: 215813, ID мероприятия
        :param order_id: "4955686", ID заказа
        :param reg_date: "2015-07-24 19:04:37", Дата заказа билета
        :param status: Статус заказа в машиночитаемом формате
        :param email: "test-mail@ya.ru", E-mail заказчика
        :param surname: "Смирнов", Фамилия на билете
        :param name: "Владимир", Имя на билете
        :param printed_id: "5184211:83845994", ID билета 
            (печататется на самом билете)
        :return: int Rows affected 
        
        """
        if status == Ticket.STATUS_NEW:
            ticket = self.create_ticket(
                order_id=order_id,
                event_id=event_id, 
                status=status, 
                reg_date=reg_date,
                email=email,
                name=name,
                surname=surname,
                printed_id=printed_id,
            )
            if ticket:
                return 1
            else:
                return 0
        else:
            try:
                ticket = self.get(order_id=order_id, event_id=event_id)
                send_template(
                    template_name=self.status_to_template(ticket.status),
                    email=ticket.email,
                    surname=ticket.surname,
                    name=ticket.name,
                )
                return 1
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                return 0

    def set_status_canceled(self, *, order_id, event_id, **kwargs):
        " Set ticket status to canceled."
        tickets = self.filter(order_id=order_id, event_id=event_id)
        for ticket in tickets:
            send_template(
                template_name="ticket-cancel",
                email=ticket.email,
                surname=ticket.surname,
                name=ticket.name,
            )
        tickets.update(status=Ticket.STATUS_CANCELED)

class Ticket(models.Model):
    """ Ticket from the timepad.

        :param event_id: 215813, ID мероприятия
        :param order_id: "4955686", ID заказа
        :param reg_date: "2015-07-24 19:04:37", Дата заказа билета
        :param status: Статус заказа в машиночитаемом формате
        :param email: "test-mail@ya.ru", E-mail заказчика
        :param surname: "Смирнов", Фамилия на билете
        :param name: "Владимир", Имя на билете
        :param printed_id: "5184211:83845994", ID билета 
            (печататется на самом билете)
    """
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
    STATUS_RAW_TO_CHOICE = {
        'ok': STATUS_PAID,  # no store, no mail
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
        return f"""
            {self.printed_id}: ID билета (печататется на самом билете)
            {self.event_id}: ID мероприятия
            {self.order_id}: ID заказа
            {self.reg_date}: Дата заказа билета
            {self.status}: Статус заказа в машиночитаемом формате
            {self.email}: E-mail заказчика
            {self.surname}: Фамилия на билете
            {self.name}: Имя на билете
            """

