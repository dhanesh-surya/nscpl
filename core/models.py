from django.db import models
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field


class HeroSlide(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    background_image = models.ImageField(upload_to="hero/")
    button_text = models.CharField(max_length=50, blank=True)
    button_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Hero Slide'
        verbose_name_plural = 'Hero Slides'

    def __str__(self):
        return self.title


class WebsiteTheme(models.Model):
    # Basic Settings
    name = models.CharField(max_length=100, default="Default Theme")
    is_active = models.BooleanField(default=True)
    
    # Color Scheme
    primary_color = models.CharField(max_length=7, default="#0A192F", help_text="Navy Blue - Main brand color")
    accent_color = models.CharField(max_length=7, default="#00BFA6", help_text="Teal - Accent color")
    secondary_color = models.CharField(max_length=7, default="#F5F5F5", help_text="Light Gray - Secondary color")
    highlight_color = models.CharField(max_length=7, default="#FF9800", help_text="Orange - Highlight color")
    
    # Background Settings
    background_type = models.CharField(
        max_length=20,
        choices=[
            ('color', 'Solid Color'),
            ('image', 'Background Image'),
            ('gradient', 'Gradient'),
        ],
        default='color'
    )
    background_color = models.CharField(max_length=7, default="#FFFFFF", help_text="Background color")
    background_image = models.ImageField(upload_to="themes/", blank=True, null=True, help_text="Background image")
    background_gradient = models.CharField(max_length=200, blank=True, help_text="CSS gradient (e.g., linear-gradient(45deg, #ff0000, #0000ff))")
    
    # Typography
    font_family = models.CharField(
        max_length=50,
        choices=[
            ('Inter', 'Inter - Modern & Clean'),
            ('Roboto', 'Roboto - Google Material'),
            ('Open Sans', 'Open Sans - Humanist'),
            ('Lato', 'Lato - Semi-rounded'),
            ('Poppins', 'Poppins - Geometric'),
            ('Montserrat', 'Montserrat - Urban'),
            ('Nunito', 'Nunito - Rounded'),
            ('Source Sans Pro', 'Source Sans Pro - Adobe'),
            ('Work Sans', 'Work Sans - Professional'),
            ('Fira Sans', 'Fira Sans - Mozilla'),
            ('IBM Plex Sans', 'IBM Plex Sans - Corporate'),
            ('Noto Sans', 'Noto Sans - Google'),
            ('Manrope', 'Manrope - Modern'),
            ('DM Sans', 'DM Sans - Editorial'),
            ('Plus Jakarta Sans', 'Plus Jakarta Sans - Indonesian'),
            ('Figtree', 'Figtree - Friendly'),
            ('Satoshi', 'Satoshi - Premium'),
            ('Cabinet Grotesk', 'Cabinet Grotesk - Display'),
            ('Space Grotesk', 'Space Grotesk - Futuristic'),
            ('Outfit', 'Outfit - Geometric'),
        ],
        default='Inter'
    )
    font_size_base = models.PositiveIntegerField(default=16, help_text="Base font size in pixels")
    heading_font_family = models.CharField(
        max_length=50,
        choices=[
            ('Inter', 'Inter - Modern & Clean'),
            ('Roboto', 'Roboto - Google Material'),
            ('Open Sans', 'Open Sans - Humanist'),
            ('Lato', 'Lato - Semi-rounded'),
            ('Poppins', 'Poppins - Geometric'),
            ('Montserrat', 'Montserrat - Urban'),
            ('Nunito', 'Nunito - Rounded'),
            ('Source Sans Pro', 'Source Sans Pro - Adobe'),
            ('Work Sans', 'Work Sans - Professional'),
            ('Fira Sans', 'Fira Sans - Mozilla'),
            ('IBM Plex Sans', 'IBM Plex Sans - Corporate'),
            ('Noto Sans', 'Noto Sans - Google'),
            ('Manrope', 'Manrope - Modern'),
            ('DM Sans', 'DM Sans - Editorial'),
            ('Plus Jakarta Sans', 'Plus Jakarta Sans - Indonesian'),
            ('Figtree', 'Figtree - Friendly'),
            ('Satoshi', 'Satoshi - Premium'),
            ('Cabinet Grotesk', 'Cabinet Grotesk - Display'),
            ('Space Grotesk', 'Space Grotesk - Futuristic'),
            ('Outfit', 'Outfit - Geometric'),
        ],
        default='Inter'
    )
    
    # Text Colors
    text_primary = models.CharField(max_length=7, default="#2C3E50", help_text="Primary text color")
    text_secondary = models.CharField(max_length=7, default="#6C757D", help_text="Secondary text color")
    text_light = models.CharField(max_length=7, default="#FFFFFF", help_text="Light text color")
    
    # Navbar Settings
    navbar_background = models.CharField(max_length=7, default="#0A192F", help_text="Navbar background color")
    navbar_text_color = models.CharField(max_length=7, default="#FFFFFF", help_text="Navbar text color")
    navbar_hover_color = models.CharField(max_length=7, default="#00BFA6", help_text="Navbar hover color")
    navbar_style = models.CharField(
        max_length=20,
        choices=[
            ('solid', 'Solid'),
            ('transparent', 'Transparent'),
            ('glass', 'Glass Effect'),
        ],
        default='solid'
    )
    
    # Button Settings
    button_style = models.CharField(
        max_length=20,
        choices=[
            ('rounded', 'Rounded'),
            ('square', 'Square'),
            ('pill', 'Pill'),
        ],
        default='rounded'
    )
    button_primary_bg = models.CharField(max_length=7, default="#0A192F", help_text="Primary button background")
    button_primary_text = models.CharField(max_length=7, default="#FFFFFF", help_text="Primary button text")
    button_secondary_bg = models.CharField(max_length=7, default="#00BFA6", help_text="Secondary button background")
    button_secondary_text = models.CharField(max_length=7, default="#FFFFFF", help_text="Secondary button text")
    
    # Link Settings
    link_color = models.CharField(max_length=7, default="#00BFA6", help_text="Link color")
    link_hover_color = models.CharField(max_length=7, default="#FF9800", help_text="Link hover color")
    link_underline = models.BooleanField(default=False, help_text="Show underline on links")
    
    # Card Settings
    card_background = models.CharField(max_length=7, default="#FFFFFF", help_text="Card background color")
    card_border_color = models.CharField(max_length=7, default="#E9ECEF", help_text="Card border color")
    card_shadow = models.BooleanField(default=True, help_text="Enable card shadows")
    card_border_radius = models.PositiveIntegerField(default=15, help_text="Card border radius in pixels")
    
    # Footer Settings
    footer_background = models.CharField(max_length=7, default="#0A192F", help_text="Footer background color")
    footer_text_color = models.CharField(max_length=7, default="#FFFFFF", help_text="Footer text color")
    footer_link_color = models.CharField(max_length=7, default="#00BFA6", help_text="Footer link color")
    
    # Layout Settings
    container_max_width = models.CharField(
        max_length=20,
        choices=[
            ('container', 'Standard'),
            ('container-fluid', 'Full Width'),
            ('container-xl', 'Extra Large'),
            ('container-lg', 'Large'),
        ],
        default='container'
    )
    section_padding = models.PositiveIntegerField(default=80, help_text="Section padding in pixels")
    
    # Animation Settings
    enable_animations = models.BooleanField(default=True, help_text="Enable AOS animations")
    animation_duration = models.PositiveIntegerField(default=800, help_text="Animation duration in milliseconds")
    
    # Custom CSS
    custom_css = models.TextField(blank=True, help_text="Custom CSS code")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Website Theme'
        verbose_name_plural = 'Website Themes'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_active:
            # Deactivate all other themes
            WebsiteTheme.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class AboutSection(models.Model):
    SECTION_CHOICES = [
        ('hero', 'Hero Section'),
        ('mission', 'Mission Section'),
        ('vision', 'Vision Section'),
        ('values', 'Values Section'),
        ('team', 'Team Section'),
        ('history', 'History Section'),
        ('achievements', 'Achievements Section'),
        ('stats', 'Stats Section'),
    ]
    
    section_type = models.CharField(max_length=20, choices=SECTION_CHOICES, unique=True)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    content = CKEditor5Field('Text', config_name='default')
    image = models.ImageField(upload_to="about/", blank=True, null=True)
    background_color = models.CharField(max_length=7, default='#FFFFFF', help_text='Hex color code')
    text_color = models.CharField(max_length=7, default='#2C3E50', help_text='Hex color code')
    
    # Section background customization fields
    section_background_type = models.CharField(
        max_length=20,
        choices=[
            ('solid', 'Solid Color'),
            ('gradient', 'Gradient'),
            ('image', 'Background Image'),
            ('pattern', 'Pattern'),
        ],
        default='solid',
        help_text="Choose the background type for this section"
    )
    section_background_color = models.CharField(max_length=7, default='#F8F9FA', help_text='Section background color')
    section_background_gradient = models.CharField(
        max_length=200, 
        blank=True, 
        help_text='CSS gradient for section background (e.g., linear-gradient(45deg, #ff0000, #0000ff))'
    )
    section_background_image = models.ImageField(
        upload_to="about/backgrounds/", 
        blank=True, 
        null=True, 
        help_text="Background image for this section"
    )
    section_background_overlay = models.CharField(
        max_length=7, 
        default='#000000', 
        help_text='Overlay color for section background image'
    )
    section_background_overlay_opacity = models.FloatField(
        default=0.3, 
        help_text='Section overlay opacity (0.0 = transparent, 1.0 = opaque)'
    )
    
    # Section animation settings
    section_animation_type = models.CharField(
        max_length=20,
        choices=[
            ('none', 'No Animation'),
            ('fade', 'Fade In'),
            ('slide', 'Slide Up'),
            ('zoom', 'Zoom In'),
            ('parallax', 'Parallax'),
        ],
        default='none',
        help_text="Animation effect for this section"
    )
    section_animation_duration = models.PositiveIntegerField(
        default=1000, 
        help_text='Section animation duration in milliseconds'
    )
    
    # Glass effect settings
    section_glass_effect = models.BooleanField(
        default=False,
        help_text='Enable glass morphism effect for this section'
    )
    section_glass_opacity = models.FloatField(
        default=0.2,
        help_text='Glass effect opacity (0.0 = transparent, 1.0 = opaque)'
    )
    section_glass_blur = models.PositiveIntegerField(
        default=10,
        help_text='Glass effect blur intensity (0-50px)'
    )
    section_glass_border = models.BooleanField(
        default=True,
        help_text='Add subtle border to glass effect'
    )
    section_glass_backdrop = models.BooleanField(
        default=True,
        help_text='Enable backdrop filter for glass effect'
    )
    
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'section_type']
        verbose_name = 'About Section'
        verbose_name_plural = 'About Sections'

    def __str__(self):
        return f"{self.get_section_type_display()} - {self.title}"
    
    def get_section_background_style(self):
        """Generate CSS background style for the section based on section_background_type"""
        if self.section_background_type == 'solid':
            return f"background-color: {self.section_background_color};"
        elif self.section_background_type == 'gradient':
            if self.section_background_gradient:
                return f"background: {self.section_background_gradient};"
            else:
                # Fallback gradient using section_background_color
                return f"background: linear-gradient(135deg, {self.section_background_color}, {self.background_color});"
        elif self.section_background_type == 'image' and self.section_background_image:
            overlay_color = self.section_background_overlay
            opacity = self.section_background_overlay_opacity
            return f"""
                background-image: linear-gradient(rgba({int(overlay_color[1:3], 16)}, {int(overlay_color[3:5], 16)}, {int(overlay_color[5:7], 16)}, {opacity})), url('{self.section_background_image.url}');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            """
        elif self.section_background_type == 'pattern':
            return f"""
                background-color: {self.section_background_color};
                background-image: radial-gradient(circle at 25px 25px, rgba(255,255,255,.2) 2px, transparent 0), radial-gradient(circle at 75px 75px, rgba(255,255,255,.2) 2px, transparent 0);
                background-size: 100px 100px;
            """
        return ""
    
    def get_section_animation_attributes(self):
        """Generate animation attributes for section template"""
        if self.section_animation_type == 'none':
            return ""
        
        attrs = f'data-aos="{self.section_animation_type}"'
        if self.section_animation_duration != 1000:
            attrs += f' data-aos-duration="{self.section_animation_duration}"'
        
        return attrs


from django_ckeditor_5.fields import CKEditor5Field

class Popup(models.Model):
    heading = models.CharField(max_length=200)
    text = CKEditor5Field('Text', config_name='default')
    image = models.ImageField(upload_to='popup_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.heading
    
    def get_section_glass_effect_style(self):
        """Generate glass effect CSS for section template"""
        if not self.section_glass_effect:
            return ""
        
        styles = []
        
        # Glass effect base styles
        styles.append(f"background: rgba(255, 255, 255, {self.section_glass_opacity});")
        
        if self.section_glass_backdrop:
            styles.append(f"backdrop-filter: blur({self.section_glass_blur}px);")
            styles.append("-webkit-backdrop-filter: blur({}px);".format(self.section_glass_blur))
        
        if self.section_glass_border:
            styles.append("border: 1px solid rgba(255, 255, 255, 0.3);")
        
        # Box shadow for depth
        styles.append("box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);")
        
        return " ".join(styles)


class Stat(models.Model):
    section = models.ForeignKey(AboutSection, on_delete=models.CASCADE, related_name='stats')
    number = models.CharField(max_length=50, help_text="The statistic number or text (e.g., '200+', '10K')")
    title = models.CharField(max_length=100, help_text="Title of the statistic (e.g., 'Projects Completed')")
    description = models.TextField(blank=True, help_text="Optional short description for the stat")
    icon = models.CharField(max_length=100, blank=True, help_text="FontAwesome icon class (e.g., 'fas fa-users')")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Stat'
        verbose_name_plural = 'Stats'

    def __str__(self):
        return f"{self.number} - {self.title}"


class Footer(models.Model):
    address = models.CharField(max_length=255, blank=True, help_text='Physical address of the organization')
    phone_number = models.CharField(max_length=20, blank=True, help_text='Contact phone number')
    email = models.EmailField(max_length=254, blank=True, help_text='Contact email address')
    facebook_url = models.URLField(blank=True, help_text='URL to Facebook profile')
    twitter_url = models.URLField(blank=True, help_text='URL to Twitter profile')
    instagram_url = models.URLField(blank=True, help_text='URL to Instagram profile')
    linkedin_url = models.URLField(blank=True, help_text='URL to LinkedIn profile')
    youtube_url = models.URLField(blank=True, help_text='URL to YouTube channel')
    quick_links_json = models.JSONField(blank=True, null=True, help_text="JSON array of quick links, e.g., [{'name': 'About Us', 'url': '/about'}]")
    copyright_text = models.CharField(max_length=255, blank=True, default='© 2025 Your Organization. All rights reserved.')
    logo = models.ImageField(upload_to='footer/', blank=True, null=True, help_text='Logo to display in the footer')
    description = CKEditor5Field(blank=True, help_text='Short description or mission statement in the footer', config_name='default')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Footer Content'
        verbose_name_plural = 'Footer Content'

    def __str__(self):
        return f"Footer Content ({self.pk})"


class QuickLink(models.Model):
    footer = models.ForeignKey(Footer, on_delete=models.CASCADE, related_name='quick_links')
    name = models.CharField(max_length=100, help_text="Display name for the quick link")
    url = models.URLField(max_length=200, help_text="URL for the quick link")
    order = models.PositiveIntegerField(default=0, help_text="Order in which the link appears")

    class Meta:
        ordering = ['order']
        verbose_name = 'Quick Link'
        verbose_name_plural = 'Quick Links'

    def __str__(self):
        return self.name


class Value(models.Model):
    title = models.CharField(max_length=200, help_text="The name of the value (e.g., 'Integrity', 'Innovation')")
    description = models.TextField(help_text="Detailed description of this value")
    icon = models.CharField(max_length=100, blank=True, help_text="FontAwesome icon class (e.g., 'fas fa-heart', 'fas fa-lightbulb')")
    image = models.ImageField(upload_to="values/", blank=True, null=True, help_text="Optional image representing this value")
    color = models.CharField(max_length=7, default='#00BFA6', help_text='Hex color code for this value')
    
    # Background customization fields
    background_type = models.CharField(
        max_length=20,
        choices=[
            ('solid', 'Solid Color'),
            ('gradient', 'Gradient'),
            ('image', 'Background Image'),
        ],
        default='solid',
        help_text="Choose the background type for this value card"
    )
    background_color = models.CharField(max_length=7, default='#FFFFFF', help_text='Background color (used for solid or gradient)')
    background_gradient = models.CharField(
        max_length=200, 
        blank=True, 
        help_text='CSS gradient (e.g., linear-gradient(45deg, #ff0000, #0000ff))'
    )
    background_image = models.ImageField(
        upload_to="values/backgrounds/", 
        blank=True, 
        null=True, 
        help_text="Background image for this value card"
    )
    background_overlay = models.CharField(
        max_length=7, 
        default='#000000', 
        help_text='Overlay color for background image (with opacity)'
    )
    background_overlay_opacity = models.FloatField(
        default=0.3, 
        help_text='Overlay opacity (0.0 = transparent, 1.0 = opaque)'
    )
    
    # Animation settings
    animation_type = models.CharField(
        max_length=20,
        choices=[
            ('none', 'No Animation'),
            ('fade', 'Fade In'),
            ('slide', 'Slide Up'),
            ('zoom', 'Zoom In'),
            ('bounce', 'Bounce'),
            ('pulse', 'Pulse'),
        ],
        default='fade',
        help_text="Animation effect for this value card"
    )
    animation_delay = models.PositiveIntegerField(
        default=0, 
        help_text='Animation delay in milliseconds'
    )
    animation_duration = models.PositiveIntegerField(
        default=800, 
        help_text='Animation duration in milliseconds'
    )
    
    is_featured = models.BooleanField(default=False, help_text="Show this value prominently")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower numbers appear first)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = 'Value'
        verbose_name_plural = 'Values'

    def __str__(self):
        return self.title
    
    def get_background_style(self):
        """Generate CSS background style based on background_type"""
        if self.background_type == 'solid':
            return f"background-color: {self.background_color};"
        elif self.background_type == 'gradient':
            if self.background_gradient:
                return f"background: {self.background_gradient};"
            else:
                # Fallback gradient using background_color
                return f"background: linear-gradient(135deg, {self.background_color}, {self.color});"
        elif self.background_type == 'image' and self.background_image:
            overlay_color = self.background_overlay
            opacity = self.background_overlay_opacity
            return f"""
                background-image: linear-gradient(rgba({int(overlay_color[1:3], 16)}, {int(overlay_color[3:5], 16)}, {int(overlay_color[5:7], 16)}, {opacity})), url('{self.background_image.url}');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            """
        return ""
    
    def get_animation_attributes(self):
        """Generate animation attributes for template"""
        if self.animation_type == 'none':
            return ""
        
        attrs = f'data-aos="{self.animation_type}"'
        if self.animation_delay > 0:
            attrs += f' data-aos-delay="{self.animation_delay}"'
        if self.animation_duration != 800:
            attrs += f' data-aos-duration="{self.animation_duration}"'
        
        return attrs


class AboutTeamMember(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to="about/team/")
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    # Background customization fields
    background_type = models.CharField(
        max_length=20,
        choices=[
            ('solid', 'Solid Color'),
            ('gradient', 'Gradient'),
            ('image', 'Background Image'),
            ('pattern', 'Pattern'),
        ],
        default='solid',
        help_text="Choose the background type for this team member card"
    )
    background_color = models.CharField(max_length=7, default='#FFFFFF', help_text='Team member card background color')
    background_gradient = models.CharField(
        max_length=200, 
        blank=True, 
        help_text='CSS gradient for team member card background (e.g., linear-gradient(45deg, #ff0000, #0000ff))'
    )
    background_image = models.ImageField(
        upload_to="about/team/backgrounds/", 
        blank=True, 
        null=True, 
        help_text="Background image for this team member card"
    )
    background_overlay = models.CharField(
        max_length=7, 
        default='#000000', 
        help_text='Overlay color for team member card background image'
    )
    background_overlay_opacity = models.FloatField(
        default=0.3, 
        help_text='Team member card overlay opacity (0.0 = transparent, 1.0 = opaque)'
    )
    
    # Animation settings
    animation_type = models.CharField(
        max_length=20,
        choices=[
            ('none', 'No Animation'),
            ('fade', 'Fade In'),
            ('slide', 'Slide Up'),
            ('zoom', 'Zoom In'),
            ('bounce', 'Bounce In'),
        ],
        default='fade',
        help_text="Animation effect for this team member card"
    )
    animation_delay = models.PositiveIntegerField(
        default=0, 
        help_text='Animation delay in milliseconds'
    )
    animation_duration = models.PositiveIntegerField(
        default=1000, 
        help_text='Animation duration in milliseconds'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Team Member'
        verbose_name_plural = 'Team Members'

    def __str__(self):
        return f"{self.name} - {self.position}"
    
    def get_background_style(self):
        """Generate CSS background style for team member card"""
        if self.background_type == 'solid':
            return f"background-color: {self.background_color};"
        elif self.background_type == 'gradient':
            if self.background_gradient:
                return f"background: {self.background_gradient};"
            else:
                # Fallback gradient using background_color
                return f"background: linear-gradient(135deg, {self.background_color}, #f8f9fa);"
        elif self.background_type == 'image' and self.background_image:
            overlay_color = self.background_overlay
            opacity = self.background_overlay_opacity
            return f"""
                background-image: linear-gradient(rgba({int(overlay_color[1:3], 16)}, {int(overlay_color[3:5], 16)}, {int(overlay_color[5:7], 16)}, {opacity})), url('{self.background_image.url}');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            """
        elif self.background_type == 'pattern':
            return f"""
                background-color: {self.background_color};
                background-image: radial-gradient(circle at 25px 25px, rgba(255,255,255,.2) 2px, transparent 0), radial-gradient(circle at 75px 75px, rgba(255,255,255,.2) 2px, transparent 0);
                background-size: 100px 100px;
            """
        return ""
    
    def get_animation_attributes(self):
        """Generate animation attributes for team member card template"""
        if self.animation_type == 'none':
            return ""
        
        attrs = f'data-aos="{self.animation_type}"'
        if self.animation_duration != 1000:
            attrs += f' data-aos-duration="{self.animation_duration}"'
        if self.animation_delay > 0:
            attrs += f' data-aos-delay="{self.animation_delay}"'
        
        return attrs
