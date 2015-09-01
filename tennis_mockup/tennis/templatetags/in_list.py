__author__ = 'laurent'
from django import template
register = template.Library()


@register.filter
def in_list(var, obj):
    return var in obj