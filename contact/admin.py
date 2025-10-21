from django.contrib import admin
from django.utils.html import format_html
from django import forms
from django.urls import path
from django.shortcuts import render
from django.http import JsonResponse
from .models import ContactInfo, ContactMessage


class ContactInfoForm(forms.ModelForm):
    """Custom form for ContactInfo with enhanced map address field"""
    
    class Meta:
        model = ContactInfo
        fields = '__all__'
        widgets = {
            'map_embed_code': forms.Textarea(attrs={
                'placeholder': 'Paste your Google Maps embed iframe code here...',
                'style': 'width: 100%; height: 120px; font-family: monospace; font-size: 12px;',
                'rows': 5
            }),
            'map_address': forms.TextInput(attrs={
                'placeholder': 'Enter full address (e.g., 123 Main St, City, State, Country)',
                'style': 'width: 100%;'
            }),
            'latitude': forms.NumberInput(attrs={
                'readonly': True,
                'style': 'background-color: #f8f9fa;'
            }),
            'longitude': forms.NumberInput(attrs={
                'readonly': True,
                'style': 'background-color: #f8f9fa;'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add help text for map embed code
        self.fields['map_embed_code'].help_text = (
            "Paste the complete Google Maps embed iframe code here. "
            "Go to Google Maps → Share → Embed a map → Copy the iframe code."
        )
        # Add help text for map address
        self.fields['map_address'].help_text = (
            "Enter the full address for Google Maps. "
            "Coordinates will be automatically generated when you save."
        )


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    form = ContactInfoForm
    list_display = ['company_name', 'city', 'state', 'primary_email', 'is_active', 'updated_at']
    list_filter = ['is_active', 'country', 'created_at']
    search_fields = ['company_name', 'city', 'state', 'primary_email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('company_name', 'tagline', 'is_active')
        }),
        ('Address Information', {
            'fields': ('address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'country')
        }),
        ('Contact Methods', {
            'fields': ('primary_phone', 'secondary_phone', 'primary_email', 'secondary_email')
        }),
        ('Business Hours', {
            'fields': ('business_hours_weekdays', 'business_hours_saturday', 'business_hours_sunday', 'show_business_hours')
        }),
        ('Social Media Links', {
            'fields': ('website_url', 'facebook_url', 'twitter_url', 'linkedin_url', 'instagram_url', 'youtube_url', 'show_social_links'),
            'classes': ('collapse',)
        }),
        ('Map Settings', {
            'fields': ('map_embed_code', 'map_address', 'latitude', 'longitude', 'map_zoom', 'show_map'),
            'classes': ('collapse',)
        }),
        ('Styling', {
            'fields': ('background_color', 'text_color'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')
    
    class Media:
        css = {
            'all': ('admin/css/contact_admin.css',)
        }
        js = ('admin/js/contact_admin.js',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status', 'is_important', 'created_at']
    list_filter = ['status', 'is_important', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['status', 'is_important']
    
    fieldsets = (
        ('Message Details', {
            'fields': ('name', 'email', 'phone', 'subject', 'message')
        }),
        ('Status & Management', {
            'fields': ('status', 'is_important', 'admin_notes', 'replied_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ['name', 'email', 'phone', 'subject', 'message', 'created_at']
        return self.readonly_fields
    
    actions = ['mark_as_read', 'mark_as_replied', 'mark_as_closed']
    
    def mark_as_read(self, request, queryset):
        queryset.update(status='read')
        self.message_user(request, f'{queryset.count()} messages marked as read.')
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_replied(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='replied', replied_at=timezone.now())
        self.message_user(request, f'{queryset.count()} messages marked as replied.')
    mark_as_replied.short_description = "Mark selected messages as replied"
    
    def mark_as_closed(self, request, queryset):
        queryset.update(status='closed')
        self.message_user(request, f'{queryset.count()} messages marked as closed.')
    mark_as_closed.short_description = "Mark selected messages as closed"
