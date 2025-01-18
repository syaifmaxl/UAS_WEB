from django import template

register = template.Library()

@register.filter(name='intcomma')
def intcomma(value):
    return "{:,.2f}".format(value).replace(",", ".")

@register.filter
def intdot(value):
    return "{:,.0f}".format(value).replace(",", ".")
