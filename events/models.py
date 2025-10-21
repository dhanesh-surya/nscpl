from django.db import models
from django.utils import timezone


class Event(models.Model):
    title = models.CharField(max_length=200)
    sport = models.CharField(max_length=100)
    date = models.DateField()
    location = models.CharField(max_length=200)
    description = models.TextField()
    banner = models.ImageField(upload_to="events/")
    is_upcoming = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return self.title

    @property
    def is_past(self):
        return self.date < timezone.now().date()


class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="events/gallery/")
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', '-uploaded_at']
        verbose_name = 'Event Image'
        verbose_name_plural = 'Event Images'

    def __str__(self):
        return f"{self.event.title} - {self.caption or 'Image'}"

    def save(self, *args, **kwargs):
        # If this is set as primary, unset other primary images for this event
        if self.is_primary:
            EventImage.objects.filter(event=self.event, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)