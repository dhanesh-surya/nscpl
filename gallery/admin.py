from django.contrib import admin
from .models import Category, GalleryItem
from django.utils.html import format_html


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']
    list_editable = ['is_active']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_featured', 'uploaded_date']
    list_filter = ['category', 'is_featured', 'uploaded_date']
    search_fields = ['title', 'description', 'tags', 'category__name']
    ordering = ['-uploaded_date']
    list_editable = ['is_featured']
    date_hierarchy = 'uploaded_date'
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'image', 'video_url', 'description')
        }),
        ('Organization', {
            'fields': ('category', 'tags', 'is_featured')
        }),
    )
    readonly_fields = ['media_preview']

    def media_preview(self, obj):
        if not obj:
            return ""
        # Prefer video thumbnail if available
        thumb = None
        if getattr(obj, 'video_url', None):
            thumb = obj.youtube_thumbnail()
        if not thumb and getattr(obj, 'image', None):
            try:
                thumb = obj.image.url
            except Exception:
                thumb = None
        if thumb:
            return format_html('<img src="{}" style="max-height:120px; max-width:200px; object-fit:cover;" />', thumb)
        return ""
    media_preview.short_description = 'Preview'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')