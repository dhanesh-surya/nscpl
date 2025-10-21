from django.contrib import admin
from .models import Event, EventImage


class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 1
    fields = ['image', 'caption', 'is_primary']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'sport', 'date', 'location', 'is_upcoming', 'created_at']
    list_filter = ['sport', 'is_upcoming', 'date', 'created_at']
    search_fields = ['title', 'sport', 'location', 'description']
    ordering = ['-date']
    list_editable = ['is_upcoming']
    date_hierarchy = 'date'
    inlines = [EventImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'sport', 'date', 'location')
        }),
        ('Content', {
            'fields': ('description', 'banner')
        }),
        ('Status', {
            'fields': ('is_upcoming',)
        }),
    )


@admin.register(EventImage)
class EventImageAdmin(admin.ModelAdmin):
    list_display = ['event', 'caption', 'is_primary', 'uploaded_at']
    list_filter = ['is_primary', 'uploaded_at', 'event__sport']
    search_fields = ['event__title', 'caption']
    ordering = ['-uploaded_at']
    list_editable = ['is_primary']