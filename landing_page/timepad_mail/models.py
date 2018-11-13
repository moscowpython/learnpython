"""Timepad ticket status mailing."""
from django.db import models
from django.utils import timezone
from .send_mail_mandrill import send_template


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
    def _convert_raw_status(status_raw: str) -> str:
        " Convert status_raw to constant statuses, None on fail."
        return Ticket.STATUS_RAW_TO_CHOICE.get(status_raw, None)

    @staticmethod
    def _convert_reg_date(reg_date: str) -> timezone.datetime:
        """ Convert status_raw to constant statuses, None on fail.
            :param reg_date: "2015-07-24 19:04:37", // Дата заказа билета
            :return: timezone.datetime reg_date
        """
        return timezone.datetime.strptime(reg_date, '%Y-%m-%d %H:%M:%S')  

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
            if self.filter(order_id=order_id, event_id=event_id).exists():
                # TODO: exectional situation, double webhook
                return 0
            else:
                self.create(
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
                    template_name=Ticket.STATUS_TEMPLATE[status],
                    email=email,
                    surname=surname,
                    name=name,
                )
                return 1
        else:
            tickets = self.filter(order_id=order_id, event_id=event_id)
            for ticket in tickets:
                send_template(
                    template_name=Ticket.STATUS_TEMPLATE[status],
                    email=ticket.email,
                    surname=ticket.surname,
                    name=ticket.name,
                )
            return tickets.update(status=status)

    def set_status_canceled(self, *, order_id, event_id, **kwargs):
        " Set ticket status to canceled."
        tickets = self.filter(order_id=order_id, event_id=event_id)
        for ticket in tickets:
            result = send_template(
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
        max_length=64,
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
        unique_together = (('order_id', 'event_id',),)
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
        return 'Билет {0}, статус {1}'.format(self.ticket_id, self.status)
