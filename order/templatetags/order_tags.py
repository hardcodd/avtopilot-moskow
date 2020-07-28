from django.template import Library

from order.models import Order

register = Library()


@register.filter
def verbose_status(status):
    choices = dict(Order.STATUS_CHOICES)
    return choices.get(status, 'Неизвестен')