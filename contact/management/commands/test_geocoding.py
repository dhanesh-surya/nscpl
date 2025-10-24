from django.core.management.base import BaseCommand
from contact.models import ContactInfo


class Command(BaseCommand):
    help = 'Test geocoding functionality for ContactInfo'

    def add_arguments(self, parser):
        parser.add_argument(
            '--address',
            type=str,
            help='Address to geocode',
            default='Mumbai, Maharashtra, India'
        )

    def handle(self, *args, **options):
        address = options['address']
        
        self.stdout.write(f'Testing geocoding for address: {address}')
        
        # Create a test ContactInfo instance
        contact_info = ContactInfo()
        contact_info.map_address = address
        
        # Test geocoding
        success = contact_info.geocode_address()
        
        if success:
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Geocoding successful!\n'
                    f'   Address: {contact_info.map_address}\n'
                    f'   Latitude: {contact_info.latitude}\n'
                    f'   Longitude: {contact_info.longitude}'
                )
            )
        else:
            self.stdout.write(
                self.style.ERROR(
                    f'❌ Geocoding failed for address: {address}\n'
                    f'   Please check your Google Maps API key and internet connection.'
                )
            )
