import re

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='remove_empty_color_span')
@stringfilter
def remove_empty_color_span(value):
    """Remove empty <p><span style="color:hsl(0,0%,100%);"></span></p> blocks (and minor variants).

    Uses a regex to remove a <p> containing an empty <span> where the span's style includes
    the exact color hsl(0,0%,100%). This handles small whitespace differences and
    single/double-quoted attributes.
    """
    if not value:
        return value

    # Pattern explanation:
    # - <p> ... </p> containing only a <span ...></span>
    # - match span with style containing color:hsl(0,0%,100%) (allow quotes and whitespace)
    pattern = re.compile(
        r"<p>\s*<span[^>]*style\s*=\s*(['\"]).*?color\s*:\s*hsl\(0\s*,\s*0%\s*,\s*100%\s*\).*?\1[^>]*>\s*</span>\s*</p>",
        flags=re.IGNORECASE | re.DOTALL,
    )

    cleaned = pattern.sub('', value)
    return mark_safe(cleaned)
