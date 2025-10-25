from django.contrib import admin
from django.utils.html import format_html
from django.forms import ModelForm
from .models import Team, Player, SportPosition


class PlayerInlineForm(ModelForm):
    class Meta:
        model = Player
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'team') and self.instance.team:
            sport = self.instance.team.sport
            positions = SportPosition.objects.filter(sport=sport)
            if positions.exists():
                self.fields['position'].widget.attrs['list'] = f'positions_{sport.id}'
                self.fields['position'].widget.attrs['autocomplete'] = 'off'


class PlayerInline(admin.TabularInline):
    model = Player
    form = PlayerInlineForm
    extra = 0
    fields = ['photo_preview', 'photo', 'name', 'position', 'jersey_number', 'is_active']
    readonly_fields = ['photo_preview']

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        if obj:
            sport = obj.sport
            positions = SportPosition.objects.filter(sport=sport)
            if positions.exists():
                position_list = [f'<option value="{p.name}">{p.name}</option>' for p in positions]
                datalist = f'<datalist id="positions_{sport.id}">{"".join(position_list)}</datalist>'
                formset.datalist = datalist
        return formset

    def photo_preview(self, obj):
        if obj and obj.photo:
            return format_html('<img src="{}" style="height:48px; width:48px; object-fit:cover; border-radius:6px;" />', obj.photo.url)
        return ""
    photo_preview.short_description = 'Photo'


@admin.register(SportPosition)
class SportPositionAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'sport']
    list_filter = ['sport']
    search_fields = ['name', 'code', 'sport__name']
    ordering = ['sport', 'name']


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