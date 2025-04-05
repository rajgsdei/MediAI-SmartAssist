from django import template
from django.template.defaultfilters import date

register = template.Library()

@register.filter
def get_attribute(obj, field):
    """
    Gets an attribute of an object dynamically from a string name
    """
    if hasattr(obj, str(field)):
        attr = getattr(obj, field)
        # Handle date fields
        if hasattr(attr, 'strftime'):
            return date(attr, "M d, Y")
        return attr
    elif isinstance(obj, dict):
        return obj.get(field, '')
    return ''