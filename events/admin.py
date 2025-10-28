from django.contrib import admin
from django import forms
from .models import Event, EventImage
from django_ckeditor_5.widgets import CKEditor5Widget


class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 1
    fields = ['image', 'caption', 'is_primary']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    # Use a ModelForm to render the `description` field with CKEditor 5
    class EventAdminForm(forms.ModelForm):
        class Meta:
            model = Event
            fields = '__all__'
            widgets = {
                'description': CKEditor5Widget(attrs={
                    'class': 'django_ckeditor_5',
                    'data-field-name': 'description',
                    'data-config-name': 'default'
                })
            }

    form = EventAdminForm
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