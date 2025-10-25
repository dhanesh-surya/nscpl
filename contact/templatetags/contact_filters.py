from django import template
import re

register = template.Library()

@register.filter
def make_responsive_iframe(embed_code):
    """Make Google Maps iframe responsive by updating width and height attributes"""
    if not embed_code:
        return embed_code
    
    # Replace fixed width with 100%
    embed_code = re.sub(r'width="\d+"', 'width="100%"', embed_code)
    
    # Set height to 450px for consistency
    embed_code = re.sub(r'height="\d+"', 'height="450"', embed_code)
    
    # Add responsive styling
    embed_code = re.sub(r'style="([^"]*)"', r'style="\1; border: 0; border-radius: 20px;"', embed_code)
    
    return embed_code
