from django.core.management.base import BaseCommand
from contact.models import ContactInfo


class Command(BaseCommand):
    help = 'Create default contact information if none exists'

    def handle(self, *args, **options):
        # Check if contact info already exists
        if ContactInfo.objects.exists():
            self.stdout.write(
                self.style.WARNING('Contact information already exists. Skipping creation.')
            )
            return

        # Create default contact info
        contact_info = ContactInfo.objects.create(
            company_name="NSCPL PRIVATE LIMITED",
            tagline="Your trusted partner in sports and events management",
            address_line_1="123 Sports Avenue",
            address_line_2="Building A, Floor 2",
            city="Mumbai",
            state="Maharashtra",
            postal_code="400001",
            country="India",
            primary_phone="+91 98765 43210",
            secondary_phone="+91 98765 43211",
            primary_email="info@nscpl.com",
            secondary_email="support@nscpl.com",
            business_hours_weekdays="Monday - Friday: 9:00 AM - 6:00 PM",
            business_hours_saturday="Saturday: 10:00 AM - 4:00 PM",
            business_hours_sunday="Sunday: Closed",
            website_url="https://www.nscpl.com",
            facebook_url="https://facebook.com/nscpl",
            linkedin_url="https://linkedin.com/company/nscpl",
            instagram_url="https://instagram.com/nscpl",
            latitude=19.0760,
            longitude=72.8777,
            map_zoom=15,
            show_map=True,
            show_social_links=True,
            show_business_hours=True,
            background_color="#F8F9FA",
            text_color="#2C3E50",
            is_active=True
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created default contact information for {contact_info.company_name}'
            )
        )
