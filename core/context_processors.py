from .models import WebsiteTheme, Footer
from page_content.models import MenuItem

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


def menu_context(request):
    """Provide site menu items for the navbar. Returns a nested list of active menu items.
    If no menu items are configured, templates should fall back to default hard-coded links.
    """
    menu_qs = MenuItem.objects.filter(is_active=True, parent__isnull=True).prefetch_related('children').order_by('order')

    def serialize(item):
        return {
            'title': item.title,
            'url': item.get_absolute_url(),
            'children': [
                {
                    'title': c.title,
                    'url': c.get_absolute_url()
                } for c in item.children.filter(is_active=True).order_by('order')
            ]
        }

    menu = [serialize(i) for i in menu_qs]
    return {'site_menu': menu}
