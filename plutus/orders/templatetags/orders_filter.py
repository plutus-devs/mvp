from django import template
from orders.models import Order

register = template.Library()

@register.filter
def order_by(queryset, order):
    return queryset.order_by(order)

@register.filter
def limit(queryset, L):
    return queryset[:int(L)]

@register.filter
def is_approved(queryset):
    return queryset.filter(status__gte=Order.APPROVED)
