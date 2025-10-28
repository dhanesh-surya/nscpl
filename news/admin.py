from django.contrib import admin
from django import forms
from .models import NewsArticle
from django_ckeditor_5.widgets import CKEditor5Widget


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_published', 'published_date', 'updated_at']
    list_filter = ['is_published', 'author', 'published_date', 'updated_at']
    search_fields = ['title', 'content', 'author__username']
    ordering = ['-published_date']
    list_editable = ['is_published']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'content', 'featured_image')
        }),
        ('Author & Status', {
            'fields': ('author', 'is_published', 'published_date')
        }),
    )
    
    # Use a ModelForm to ensure the content field uses CKEditor5 with the 'default' config
    class NewsArticleAdminForm(forms.ModelForm):
        class Meta:
            model = NewsArticle
            fields = '__all__'
            widgets = {
                'content': CKEditor5Widget(attrs={
                    'class': 'django_ckeditor_5',
                    'data-field-name': 'content',
                    'data-config-name': 'default'
                })
            }

    form = NewsArticleAdminForm
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author')