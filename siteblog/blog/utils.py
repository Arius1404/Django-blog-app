from .models import *


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['start'] = '#start'
        context['comments'] = '#comments'
        context['truncate_add'] = "Читать далее"
        return context
