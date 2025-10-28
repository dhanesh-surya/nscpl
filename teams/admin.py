from django.contrib import admin
from django.utils.html import format_html
from django import forms
from django.forms import ModelForm
from .models import Team, Player, SportPosition
from page_content.admin import StyleOptionsAdminMixin
from django_ckeditor_5.widgets import CKEditor5Widget
from core.forms import ColorPickerWidget


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
class TeamAdmin(StyleOptionsAdminMixin, admin.ModelAdmin):
    list_display = ['name', 'sport', 'founded_date', 'is_active', 'created_at']
    list_filter = ['sport', 'is_active', 'founded_date', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']
    list_editable = ['is_active']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [PlayerInline]
    
    # Use a ModelForm to render the `description` field with CKEditor 5
    class TeamAdminForm(forms.ModelForm):
        class Meta:
            model = Team
            fields = '__all__'
            widgets = {
                'description': CKEditor5Widget(attrs={
                    'class': 'django_ckeditor_5',
                    'data-field-name': 'description',
                    'data-config-name': 'default'
                }),
                'contact_icon_color': ColorPickerWidget(),
                'contact_icon_bg': ColorPickerWidget(),
            }

    form = TeamAdminForm
    readonly_fields = ('contact_preview',)

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
        ('Contact', {
            'fields': ('contact_email', 'contact_phone', 'contact_linkedin', 'contact_twitter', 'contact_icon_color', 'contact_icon_bg', 'contact_preview'),
            'classes': ('collapse',)
        }),
    )

    def contact_preview(self, obj):
        """Render a small preview with Font Awesome icons and links for contact fields."""
        if not obj:
            return ""
        parts = []
        try:
            if obj.contact_email:
                parts.append(f"<a href=\"mailto:{obj.contact_email}\" class=\"me-3 text-decoration-none\"><i class=\"fas fa-envelope\"></i></a>")
            if obj.contact_phone:
                parts.append(f"<a href=\"tel:{obj.contact_phone}\" class=\"me-3 text-decoration-none\"><i class=\"fas fa-phone\"></i></a>")
            if obj.contact_linkedin:
                parts.append(f"<a href=\"{obj.contact_linkedin}\" target=\"_blank\" rel=\"noopener\" class=\"me-3 text-decoration-none\"><i class=\"fab fa-linkedin\"></i></a>")
            if obj.contact_twitter:
                parts.append(f"<a href=\"{obj.contact_twitter}\" target=\"_blank\" rel=\"noopener\" class=\"me-3 text-decoration-none\"><i class=\"fab fa-twitter\"></i></a>")
        except Exception:
            pass
        return format_html(''.join(parts))
    contact_preview.short_description = 'Contact preview'


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