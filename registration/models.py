from django.db import models
from django.utils import timezone

class PlayerRegistration(models.Model):
    venue = models.CharField(max_length=255, verbose_name="Venue", default="")
    date_of_event = models.DateField(verbose_name="Date of Event", default=timezone.now)
    # Player Information
    sur_name = models.CharField(max_length=100, verbose_name="SUR NAME")
    first_name = models.CharField(max_length=100, verbose_name="FIRST NAME")
    fathers_name = models.CharField(max_length=100, verbose_name="FATHER'S NAME")
    date_of_birth = models.DateField(verbose_name="Date Of Birth")
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], verbose_name="Gender", default='Male')
    address = models.TextField(verbose_name="Address", default="")
    city = models.CharField(max_length=100, verbose_name="City", default="")
    state = models.CharField(max_length=100, verbose_name="State", default="")
    zip_code = models.CharField(max_length=10, verbose_name="Zip Code", default="")
    country = models.CharField(max_length=100, default="India", verbose_name="Country")
    email = models.EmailField(unique=True, verbose_name="Email", default="example@example.com")
    phone_number = models.CharField(max_length=15, verbose_name="Contact No.", default="")
    whatsapp_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Whatsapp No.")
    photo = models.ImageField(upload_to='players_photos/', blank=True, null=True, verbose_name="Player's Photo")
    approved = models.BooleanField(default=False)

    # Proficiency
    FASTER_BOWLER_CHOICES = [
        ('Right arm', 'Right arm'),
        ('Left arm', 'Left arm'),
    ]
    SPIN_BOWLER_CHOICES = [
        ('Right arm off break', 'Right arm off break'),
        ('Left arm off break', 'Left arm off break'),
        ('Right arm leg break', 'Right arm leg break'),
    ]
    BATTING_PROFICIENCY_CHOICES = [
        ('Right Hand Batter', 'Right Hand Batter'),
        ('Left Hand Batter', 'Left Hand Batter'),
    ]

    faster_bowler = models.CharField(max_length=50, choices=FASTER_BOWLER_CHOICES, blank=True, null=True, verbose_name="Faster Bowlers")
    spin_bowler = models.CharField(max_length=50, choices=SPIN_BOWLER_CHOICES, blank=True, null=True, verbose_name="Spin Bowlers")
    batting_proficiency = models.CharField(max_length=50, choices=BATTING_PROFICIENCY_CHOICES, blank=True, null=True, verbose_name="Batting Proficiency")

    # Playing Role
    PLAYING_ROLE_CHOICES = [
        ('Opening Batter', 'Opening Batter'),
        ('Middle Order Batter', 'Middle Order Batter'),
        ('Batting All Rounder', 'Batting All Rounder'),
        ('Bowling All Rounder', 'Bowling All Rounder'),
        ('Wicket Keeper', 'Wicket Keeper'),
    ]
    primary_playing_role = models.CharField(max_length=50, choices=PLAYING_ROLE_CHOICES, verbose_name="Primary Playing Role", default="Opening Batter")
    secondary_playing_role = models.CharField(max_length=50, choices=PLAYING_ROLE_CHOICES, blank=True, null=True, verbose_name="Secondary Playing Role")

    # Declarations
    physically_fit = models.BooleanField(verbose_name="Are you physically fit (in all aspects) to attend the trials?", default=False)
    declaration_past_tournament = models.BooleanField(verbose_name="I hereby declare that I have not played in any of the hard ball cricket tournament in the past.", default=False)
    declaration_parents_aware = models.BooleanField(verbose_name="I hereby declare that my parents are aware of my participation in the trial and have no objection of whatsoever. I have informed my parents about the rules / terms and condition of the event and that they indorse my signing of this declaration on there behalf as well.", default=False)
    declaration_indemnify_organizers = models.BooleanField(verbose_name="I hereby indemnify the organizers (and all associated of the organizers) from any casualty / mishap/any loss to me / my property during the process of attending the trials.", default=False)
    declaration_emergency_care = models.BooleanField(verbose_name="I hereby give my consent for emergency medical care prescribed by authorized doctor and that this care may be giving under whatever condition are necessary to preserve the my life our well-being .the costs shall be come by me /my family.", default=False)
    declaration_photo_video_consent = models.BooleanField(verbose_name="I hereby give my consent to the organizer to take photographs video recording and / or sound recording of my participation in documenting the activities.", default=False)
    declaration_true_info = models.BooleanField(verbose_name="I hereby declare that all the details given above in the registration form are true and correct to the best of my knowledge and belief . In the event of any information being found false or incorrect or myself being found not eligible in terms of eligibility criteria for the participation . My name is liable to be cancelled without any notice.", default=False)

    # Payment Information
    transaction_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="Transaction ID")
    transaction_screenshot = models.ImageField(upload_to='transactions/', blank=True, null=True, verbose_name="Transaction Screenshot")

    registration_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.first_name} {self.sur_name} - {self.primary_playing_role}"


class RegistrationPageSetting(models.Model):
    """Stores styling options for the registration page which can be edited in the admin."""
    name = models.CharField(max_length=100, default='Default')
    is_active = models.BooleanField(default=False, help_text='Mark this as the active registration page setting')

    primary_color = models.CharField(max_length=7, default="#0A192F")
    accent_color = models.CharField(max_length=7, default="#00BFA6")
    background_color = models.CharField(max_length=7, default="#FFFFFF")
    text_color = models.CharField(max_length=7, default="#2C3E50")
    heading_color = models.CharField(max_length=7, default="#0A192F", help_text='Color for the registration page heading')
    subtitle_color = models.CharField(max_length=7, default="#6C757D", help_text='Color for the registration page subtitle')

    button_primary_bg = models.CharField(max_length=7, default="#0A192F")
    button_primary_text = models.CharField(max_length=7, default="#FFFFFF")

    card_background = models.CharField(max_length=7, default="#FFFFFF")
    card_border_color = models.CharField(max_length=7, default="#E9ECEF")
    card_border_radius = models.PositiveIntegerField(default=8)

    font_family = models.CharField(max_length=50, default='Inter')
    font_size_base = models.PositiveIntegerField(default=16)

    custom_css = models.TextField(blank=True, help_text='Optional custom CSS to apply to the registration page')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Registration Page Setting'
        verbose_name_plural = 'Registration Page Settings'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # If this instance is set active, deactivate other settings
        if self.is_active:
            RegistrationPageSetting.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)
