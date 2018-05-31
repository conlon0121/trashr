from django import template
from django.utils import timezone
from dateutil.relativedelta import relativedelta


register = template.Library()


@register.filter
def get_color(l, index):
    try:
        return l[index]
    except:
        return None


@register.filter
def to_dollars(value):
    try:
        dollars = round(value / 100, 2)
        return '$%.2f' % dollars
    except (ValueError, ZeroDivisionError):
        return None


@register.filter
def multiply(value, arg):
    return value * arg


@register.filter
def add_one_month_to_now(value):
    date = timezone.now()
    if date.day > value:
        date = date + relativedelta(months=1)
    date = date.replace(day=25)
    return date.date()


@register.filter
def sort_by_subscription(values, sub):
    top = sub.payment_method
    values = list(values)
    index_top = values.index(top)
    if index_top == 0:
        return values
    swap_index = 0
    values[index_top], values[swap_index] = values[swap_index], values[index_top]
    return values

