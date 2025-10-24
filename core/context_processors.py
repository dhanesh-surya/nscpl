from .models import WebsiteTheme, Footer

def theme_context(request):
    """
    Add the active theme to the context for all templates
    """
    theme = WebsiteTheme.objects.filter(is_active=True).first()
    return {
        'theme': theme
    }

def footer_context(request):
    """
    Add the footer object to the context for all templates
    """
    footer = Footer.objects.prefetch_related('quick_links').first()
    return {
        'footer': footer
    }
