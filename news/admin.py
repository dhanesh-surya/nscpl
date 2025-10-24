from django.contrib import admin
from .models import NewsArticle


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
            'fields': ('author', 'is_published')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author')