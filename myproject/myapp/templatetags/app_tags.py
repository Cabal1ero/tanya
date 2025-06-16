from django import template
from myapp.models import Service

register = template.Library()

@register.inclusion_tag('partials/booking_form.html')
def booking_form():
    services = Service.objects.all()
    return {'services': services}

@register.filter(name='reverselist')
def reverselist(value):
    return value[::-1] 