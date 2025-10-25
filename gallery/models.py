from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class GalleryItem(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="gallery/", blank=True, null=True)
    video_url = models.URLField(blank=True, null=True, help_text='YouTube video URL (optional)')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags")
    description = models.TextField(blank=True)
    uploaded_date = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-uploaded_date']
        verbose_name = 'Gallery Item'
        verbose_name_plural = 'Gallery Items'

    def __str__(self):
        return self.title

    def youtube_thumbnail(self):
        """Return a YouTube thumbnail URL if video_url is present and looks like a YouTube link."""
        if not self.video_url:
            return None
        # Try to extract video id from common YouTube URL formats
        import re
        patterns = [
            r'youtu\.be/(?P<id>[A-Za-z0-9_-]{11})',
            r'v=(?P<id>[A-Za-z0-9_-]{11})',
            r'embed/(?P<id>[A-Za-z0-9_-]{11})',
        ]
        for p in patterns:
            m = re.search(p, self.video_url)
            if m:
                vid = m.group('id')
                return f'https://img.youtube.com/vi/{vid}/hqdefault.jpg'
        return None

    @property
    def tag_list(self):
        """Return tags as a list"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []