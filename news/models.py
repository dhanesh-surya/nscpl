from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field


class NewsArticle(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = CKEditor5Field('Text', config_name='extends')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news_articles')
    featured_image = models.ImageField(upload_to="news/", blank=True, null=True)
    is_published = models.BooleanField(default=False)
    published_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date']
        verbose_name = 'News Article'
        verbose_name_plural = 'News Articles'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)