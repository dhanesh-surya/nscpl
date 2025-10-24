from django.core.management.base import BaseCommand
from core.models import WebsiteTheme


class Command(BaseCommand):
    help = 'Create a default theme if none exists'

    def handle(self, *args, **options):
        # Check if any theme exists
        if not WebsiteTheme.objects.exists():
            # Create default theme
            default_theme = WebsiteTheme.objects.create(
                name="Default NSCPL Theme",
                is_active=True,
                primary_color="#0A192F",
                accent_color="#00BFA6",
                secondary_color="#F5F5F5",
                highlight_color="#FF9800",
                background_type="color",
                background_color="#FFFFFF",
                font_family="Inter",
                font_size_base=16,
                heading_font_family="Inter",
                text_primary="#2C3E50",
                text_secondary="#6C757D",
                text_light="#FFFFFF",
                navbar_background="#0A192F",
                navbar_text_color="#FFFFFF",
                navbar_hover_color="#00BFA6",
                navbar_style="solid",
                button_style="rounded",
                button_primary_bg="#00BFA6",
                button_primary_text="#FFFFFF",
                button_secondary_bg="#6C757D",
                button_secondary_text="#FFFFFF",
                link_color="#00BFA6",
                link_hover_color="#FF9800",
                link_underline=False,
                card_background="#FFFFFF",
                card_border_color="#E9ECEF",
                card_shadow=True,
                card_border_radius=8,
                footer_background="#0A192F",
                footer_text_color="#FFFFFF",
                footer_link_color="#00BFA6",
                container_max_width="1200px",
                section_padding=80,
                enable_animations=True,
                animation_duration=500
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created default theme: {default_theme.name}')
            )
        else:
            # Ensure at least one theme is active
            active_themes = WebsiteTheme.objects.filter(is_active=True)
            if not active_themes.exists():
                first_theme = WebsiteTheme.objects.first()
                first_theme.is_active = True
                first_theme.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Activated theme: {first_theme.name}')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS('Theme already exists and is active')
                )
