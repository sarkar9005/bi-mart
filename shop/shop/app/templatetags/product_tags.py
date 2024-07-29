# product/templatetags/custom_tags.py
from django import template

register = template.Library()

@register.simple_tag
def get_dict_value(dictionary, key):
    return dictionary.get(key, '')
