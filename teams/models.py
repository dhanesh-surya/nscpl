from django.db import models
from django.utils.text import slugify
from django.db import models as dj_models
from page_content.models import StyleOptions


class Team(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    sport = models.ForeignKey('sports.Sport', on_delete=models.CASCADE, related_name='teams')
    logo = models.ImageField(upload_to="teams/logos/", blank=True, null=True)
    description = models.TextField(blank=True)
    founded_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Styling options for team cards and sections
    style_options = dj_models.OneToOneField(
        'page_content.StyleOptions', on_delete=dj_models.SET_NULL,
        null=True, blank=True, help_text='Custom styling options for this team'
    )
    # Contact information
    contact_email = models.EmailField(max_length=254, blank=True, help_text='Contact email for the team')
    contact_phone = models.CharField(max_length=30, blank=True, help_text='Contact phone number for the team')
    contact_linkedin = models.URLField(blank=True, help_text='LinkedIn profile or page URL for the team')
    contact_twitter = models.URLField(blank=True, help_text='Twitter profile URL for the team')
    # Contact icon colors
    contact_icon_color = models.CharField(max_length=7, default='#212529', blank=True, help_text='Hex color for contact icons (e.g., #ffffff)')
    contact_icon_bg = models.CharField(max_length=7, default='', blank=True, help_text='Optional background color for icon buttons (hex)')

    class Meta:
        ordering = ['name']
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        # Ensure style_options exists for the team
        if not self.style_options:
            so = StyleOptions.objects.create()
            self.style_options = so
        super().save(*args, **kwargs)


class SportPosition(models.Model):
    sport = models.ForeignKey('sports.Sport', on_delete=models.CASCADE, related_name='positions')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)

    class Meta:
        ordering = ['sport', 'name']
        verbose_name = 'Sport Position'
        verbose_name_plural = 'Sport Positions'
        unique_together = ['sport', 'code']

    def __str__(self):
        return f"{self.name} ({self.sport.name})"


class Player(models.Model):
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    position = models.CharField(max_length=100)
    jersey_number = models.PositiveIntegerField(blank=True, null=True)
    photo = models.ImageField(upload_to="players/photos/", blank=True, null=True)
    bio = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['jersey_number', 'name']
        verbose_name = 'Player'
        verbose_name_plural = 'Players'

    def __str__(self):
        return f"{self.name} ({self.team.name})"