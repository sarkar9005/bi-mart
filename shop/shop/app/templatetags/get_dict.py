from django import template

register = template.Library()

@register.filter(name="get_val")
def get_val(value, arg):
    return value.get(arg)