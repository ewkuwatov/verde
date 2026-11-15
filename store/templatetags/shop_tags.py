from django import template

register = template.Library()


@register.filter
def currency(value):
    try:
        amount = int(value)
    except (TypeError, ValueError):
        return value
    return f"{amount:,}".replace(",", " ")


@register.filter
def mul(value, multiplier):
    try:
        return value * int(multiplier)
    except (TypeError, ValueError):
        return value
