from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiplies the value with the arg."""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        try:
            return float(value) * float(arg)
        except (ValueError, TypeError):
            return ''