from django.db import models
from django.utils.text import slugify


class ContactInfo(models.Model):
    """Model to store contact information that can be managed through Django admin"""
    
    # Basic Information
    company_name = models.CharField(max_length=200, default="NSCPL PRIVATE LIMITED")
    tagline = models.CharField(max_length=300, blank=True, help_text="Short tagline or description")
    
    # Contact Details
    address_line_1 = models.CharField(max_length=200, help_text="Street address")
    address_line_2 = models.CharField(max_length=200, blank=True, help_text="Apartment, suite, etc.")
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default="India")
    
    # Contact Methods
    primary_phone = models.CharField(max_length=20, help_text="Main contact number")
    secondary_phone = models.CharField(max_length=20, blank=True, help_text="Alternative contact number")
    primary_email = models.EmailField(help_text="Main contact email")
    secondary_email = models.EmailField(blank=True, help_text="Alternative contact email")
    
    # Business Hours
    business_hours_weekdays = models.CharField(
        max_length=100, 
        default="Monday - Friday: 9:00 AM - 6:00 PM",
        help_text="Weekday business hours"
    )
    business_hours_saturday = models.CharField(
        max_length=100, 
        default="Saturday: 10:00 AM - 4:00 PM",
        help_text="Saturday business hours"
    )
    business_hours_sunday = models.CharField(
        max_length=100, 
        default="Sunday: Closed",
        help_text="Sunday business hours"
    )
    
    # Social Media Links
    website_url = models.URLField(blank=True, help_text="Company website URL")
    facebook_url = models.URLField(blank=True, help_text="Facebook page URL")
    twitter_url = models.URLField(blank=True, help_text="Twitter profile URL")
    linkedin_url = models.URLField(blank=True, help_text="LinkedIn company page URL")
    instagram_url = models.URLField(blank=True, help_text="Instagram profile URL")
    youtube_url = models.URLField(blank=True, help_text="YouTube channel URL")
    
    # Map Settings
    map_embed_code = models.TextField(
        blank=True, 
        help_text="Google Maps embed iframe code (paste the full iframe tag here)"
    )
    map_address = models.CharField(
        max_length=500, 
        blank=True, 
        help_text="Full address for Google Maps (will auto-populate coordinates)"
    )
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        blank=True, 
        null=True,
        help_text="Latitude for map display (auto-generated from address)"
    )
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        blank=True, 
        null=True,
        help_text="Longitude for map display (auto-generated from address)"
    )
    map_zoom = models.PositiveIntegerField(
        default=15,
        help_text="Map zoom level (1-20)"
    )
    
    # Display Settings
    show_map = models.BooleanField(default=True, help_text="Show map on contact page")
    show_social_links = models.BooleanField(default=True, help_text="Show social media links")
    show_business_hours = models.BooleanField(default=True, help_text="Show business hours")
    
    # Styling
    background_color = models.CharField(
        max_length=7, 
        default='#F8F9FA', 
        help_text='Contact section background color'
    )
    text_color = models.CharField(
        max_length=7, 
        default='#2C3E50', 
        help_text='Contact section text color'
    )
    
    # Status
    is_active = models.BooleanField(default=True, help_text="Enable/disable contact information")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Contact Information'
        verbose_name_plural = 'Contact Information'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.company_name} - Contact Info"
    
    def get_full_address(self):
        """Return formatted full address"""
        address_parts = [self.address_line_1]
        if self.address_line_2:
            address_parts.append(self.address_line_2)
        address_parts.extend([self.city, self.state, self.postal_code, self.country])
        return ', '.join(filter(None, address_parts))
    
    def get_primary_contact(self):
        """Return primary contact information"""
        return {
            'phone': self.primary_phone,
            'email': self.primary_email
        }
    
    def get_social_links(self):
        """Return active social media links"""
        social_links = {}
        if self.website_url:
            social_links['website'] = self.website_url
        if self.facebook_url:
            social_links['facebook'] = self.facebook_url
        if self.twitter_url:
            social_links['twitter'] = self.twitter_url
        if self.linkedin_url:
            social_links['linkedin'] = self.linkedin_url
        if self.instagram_url:
            social_links['instagram'] = self.instagram_url
        if self.youtube_url:
            social_links['youtube'] = self.youtube_url
        return social_links
    
    def geocode_address(self):
        """Geocode the map_address to get latitude and longitude"""
        if not self.map_address:
            return False
        
        try:
            import requests
            from django.conf import settings
            
            # Use Google Geocoding API
            api_key = getattr(settings, 'GOOGLE_MAPS_API_KEY', None)
            if not api_key:
                return False
            
            url = f"https://maps.googleapis.com/maps/api/geocode/json"
            params = {
                'address': self.map_address,
                'key': api_key
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if data['status'] == 'OK' and data['results']:
                location = data['results'][0]['geometry']['location']
                self.latitude = location['lat']
                self.longitude = location['lng']
                return True
            else:
                return False
                
        except Exception as e:
            print(f"Geocoding error: {e}")
            return False
    
    def save(self, *args, **kwargs):
        # Auto-geocode if map_address is provided and coordinates are not set
        if self.map_address and (not self.latitude or not self.longitude):
            self.geocode_address()
        super().save(*args, **kwargs)


class ContactMessage(models.Model):
    """Model to store contact form submissions"""
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('closed', 'Closed'),
    ]
    
    # Contact Details
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    
    # Status and Management
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='new'
    )
    is_important = models.BooleanField(default=False, help_text="Mark as important message")
    admin_notes = models.TextField(blank=True, help_text="Internal notes about this message")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    replied_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject} ({self.get_status_display()})"
    
    def get_short_message(self, length=100):
        """Return truncated message for display"""
        if len(self.message) <= length:
            return self.message
        return self.message[:length] + "..."
