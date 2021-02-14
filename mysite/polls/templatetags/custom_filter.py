# -*- coding: utf-8 -*-
from django.template import Library
register = Library()

@register.filter
def convert_str_percent (v, ) :
    try :
        return str(v*10, ) + "%"
    except ValueError :
        return None