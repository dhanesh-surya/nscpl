from django.contrib import admin
from .models import Team, Player


class PlayerInline(admin.TabularInline):
    model = Player
    extra = 0
    fields = ['name', 'position', 'jersey_number', 'is_active']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'sport', 'founded_date', 'is_active', 'created_at']
    list_filter = ['sport', 'is_active', 'founded_date', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']
    list_editable = ['is_active']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [PlayerInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'sport', 'description')
        }),
        ('Media', {
            'fields': ('logo',)
        }),
        ('Details', {
            'fields': ('founded_date',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['name', 'team', 'position', 'jersey_number', 'is_active']
    list_filter = ['team', 'position', 'is_active', 'created_at']
    search_fields = ['name', 'team__name']
    ordering = ['team', 'jersey_number', 'name']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'team', 'position', 'jersey_number')
        }),
        ('Media', {
            'fields': ('photo',)
        }),
        ('Details', {
            'fields': ('bio',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )