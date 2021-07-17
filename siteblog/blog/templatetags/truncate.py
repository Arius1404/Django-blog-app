from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def truncate(value, end):
    words = value.split()
    keep = words[0:end]
    keep[end-1] = keep[end-1]+"... Читать далее"
    return " ".join(keep)
