from django.contrib import admin
from .models import Sport


@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']
    list_editable = ['is_active']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'rules_and_regulations', 'history')
        }),
        ('Media', {
            'fields': ('icon', 'image')
        }),
        ('Visibility', {
            'fields': ('is_active', 'show_rules_and_regulations', 'show_history')
        }),
    )