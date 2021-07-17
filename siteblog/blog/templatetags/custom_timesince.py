from datetime import timedelta
from django import template
from django.utils import timezone
from django.utils.timesince import timesince

register = template.Library()


@register.simple_tag
def custom_timesince(value):
    now = timezone.now()
    diff = now - value
    if diff > timedelta(hours=1):
        return timesince(value).split(", ")[0]
    else:
        return "Менее часа назад"
