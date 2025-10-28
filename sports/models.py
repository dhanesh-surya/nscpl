from django.db import models
from django.utils.text import slugify


class Sport(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    from django_ckeditor_5.fields import CKEditor5Field

    description = CKEditor5Field(blank=True, null=True, config_name='default')
    rules_and_regulations = CKEditor5Field(blank=True, null=True, config_name='default')
    history = CKEditor5Field(blank=True, null=True, config_name='default')
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class (e.g., 'fas fa-football-ball')")
    image = models.ImageField(upload_to="sports/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    show_rules_and_regulations = models.BooleanField(default=True)
    show_history = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Sport'
        verbose_name_plural = 'Sports'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)