from django import forms
from django.utils.html import format_html


class FontPreviewSelect(forms.Select):
    """
    Simple font preview widget that shows preview beside font name
    """
    def __init__(self, attrs=None, choices=()):
        default_attrs = {
            'class': 'font-preview-select',
            'style': 'font-family: inherit;'
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs, choices)
    
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        
        # Add font preview to the option label
        if value and label:
            option['label'] = format_html(
                '{} <span style="font-family: \'{}\', sans-serif; color: #666; font-size: 12px;">(Sample Text)</span>',
                label,
                value
            )
        
        return option
