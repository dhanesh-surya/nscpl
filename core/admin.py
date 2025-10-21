from django.contrib import admin
from django import forms
from django.urls import reverse
from django.utils.html import format_html
from .models import HeroSlide, WebsiteTheme, AboutSection, AboutTeamMember, Value, Stat, Footer, QuickLink, Popup
from .widgets import FontPreviewSelect
from .forms import (
    HeroSectionForm, MissionSectionForm,
    ValuesSectionForm, TeamSectionForm, HistorySectionForm,
    AchievementsSectionForm, AboutSectionForm, ValueForm
)
from .forms import WebsiteThemeForm, AboutSectionForm, HeroSectionForm, MissionSectionForm, ValuesSectionForm, TeamSectionForm, HistorySectionForm, AchievementsSectionForm, ValueForm, AboutTeamMemberForm, StatForm, FooterForm


class ColorPickerWidget(forms.TextInput):
    input_type = 'color'
    
    def __init__(self, attrs=None):
        default_attrs = {
            'class': 'form-control',
            'style': 'width: 80px; height: 40px; border: none; border-radius: 8px; cursor: pointer;'
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)


class WebsiteThemeForm(forms.ModelForm):
    class Meta:
        model = WebsiteTheme
        fields = '__all__'
        widgets = {
            'primary_color': ColorPickerWidget(),
            'accent_color': ColorPickerWidget(),
            'secondary_color': ColorPickerWidget(),
            'highlight_color': ColorPickerWidget(),
            'background_color': ColorPickerWidget(),
            'text_primary': ColorPickerWidget(),
            'text_secondary': ColorPickerWidget(),
            'text_light': ColorPickerWidget(),
            'navbar_background': ColorPickerWidget(),
            'navbar_text_color': ColorPickerWidget(),
            'navbar_hover_color': ColorPickerWidget(),
            'button_primary_bg': ColorPickerWidget(),
            'button_primary_text': ColorPickerWidget(),
            'button_secondary_bg': ColorPickerWidget(),
            'button_secondary_text': ColorPickerWidget(),
            'link_color': ColorPickerWidget(),
            'link_hover_color': ColorPickerWidget(),
            'card_background': ColorPickerWidget(),
            'card_border_color': ColorPickerWidget(),

            'footer_background': ColorPickerWidget(),
            'footer_text_color': ColorPickerWidget(),
            'footer_link_color': ColorPickerWidget(),
            'font_family': FontPreviewSelect(),
            'heading_font_family': FontPreviewSelect(),
        }



class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order', 'button_text', 'button_url', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('order', '-created_at')
    list_editable = ('is_active', 'order')
    readonly_fields = ('created_at', 'updated_at')



class WebsiteThemeAdmin(admin.ModelAdmin):
    form = WebsiteThemeForm
    list_display = ('name', 'is_active', 'primary_color', 'accent_color', 'font_family', 'created_at')
    list_filter = ('is_active', 'font_family', 'background_type', 'navbar_style', 'button_style')
    search_fields = ('name', 'font_family')
    ordering = ('-is_active', '-created_at')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Settings', {
            'fields': ('name', 'is_active'),
            'classes': ('wide',)
        }),
        ('Color Scheme', {
            'fields': (
                ('primary_color', 'accent_color'),
                ('secondary_color', 'highlight_color'),
            ),
            'classes': ('wide',),
            'description': 'Choose your main brand colors'
        }),
        ('Background Settings', {
            'fields': (
                'background_type',
                ('background_color', 'background_image'),
                'background_gradient'
            ),
            'classes': ('wide',),
            'description': 'Configure the website background'
        }),
        ('Typography', {
            'fields': (
                ('font_family', 'heading_font_family'),
                'font_size_base'
            ),
            'classes': ('wide',),
            'description': 'Set fonts and text sizing'
        }),
        ('Text Colors', {
            'fields': (
                ('text_primary', 'text_secondary'),
                'text_light'
            ),
            'classes': ('wide',),
            'description': 'Configure text colors throughout the site'
        }),
        ('Navbar Settings', {
            'fields': (
                ('navbar_background', 'navbar_text_color'),
                ('navbar_hover_color', 'navbar_style')
            ),
            'classes': ('wide',),
            'description': 'Customize the navigation bar appearance'
        }),
        ('Button Settings', {
            'fields': (
                'button_style',
                ('button_primary_bg', 'button_primary_text'),
                ('button_secondary_bg', 'button_secondary_text')
            ),
            'classes': ('wide',),
            'description': 'Style buttons and interactive elements'
        }),
        ('Link Settings', {
            'fields': (
                ('link_color', 'link_hover_color'),
                'link_underline'
            ),
            'classes': ('wide',),
            'description': 'Configure link appearance and behavior'
        }),
        ('Card Settings', {
            'fields': (
                ('card_background', 'card_border_color'),
                ('card_shadow', 'card_border_radius')
            ),
            'classes': ('wide',),
            'description': 'Style cards and content containers'
        }),
        ('Footer Settings', {
            'fields': (
                ('footer_background', 'footer_text_color'),
                'footer_link_color'
            ),
            'classes': ('wide',),
            'description': 'Customize the footer appearance'
        }),
        ('Layout Settings', {
            'fields': (
                'container_max_width',
                'section_padding'
            ),
            'classes': ('wide',),
            'description': 'Control overall layout and spacing'
        }),
        ('Animation Settings', {
            'fields': (
                'enable_animations',
                'animation_duration'
            ),
            'classes': ('wide',),
            'description': 'Configure animations and transitions'
        }),
        ('Custom CSS', {
            'fields': ('custom_css',),
            'classes': ('wide',),
            'description': 'Add custom CSS code for advanced styling'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if obj.is_active:
            # Deactivate all other themes
            WebsiteTheme.objects.filter(is_active=True).exclude(pk=obj.pk).update(is_active=False)
        super().save_model(request, obj, form, change)








class StatInline(admin.TabularInline):
    model = Stat
    extra = 1
    fields = ('title', 'number', 'order', 'is_active')


class StatInline(admin.TabularInline):
    model = Stat
    extra = 1
    fields = ('title', 'number', 'order', 'is_active')



class AboutSectionAdmin(admin.ModelAdmin):
    form = AboutSectionForm
    change_form_template = "admin/core/aboutsection/change_form.html"
    list_display = ('title', 'section_type', 'is_active', 'order', 'updated_at')
    list_filter = ('section_type', 'is_active')
    search_fields = ('title', 'subtitle', 'content')
    ordering = ('order', 'title')
    fieldsets = (
        (None, {
            'fields': ('section_type', 'title', 'subtitle', 'content', 'image', 'is_active', 'order')
        }),
        ('Styling Options', {
            'fields': ('background_color', 'text_color'),
            'classes': ('collapse',)
        }),
        ('Section Background', {
            'fields': (
                'section_background_type', 'section_background_color', 'section_background_gradient',
                'section_background_image', 'section_background_overlay', 'section_background_overlay_opacity',
            ),
            'classes': ('collapse',)
        }),
        ('Section Animation', {
            'fields': ('section_animation_type', 'section_animation_duration'),
            'classes': ('collapse',)
        }),
        ('Section Glass Effect', {
            'fields': (
                'section_glass_effect', 'section_glass_opacity', 'section_glass_blur',
                'section_glass_border', 'section_glass_backdrop',
            ),
            'classes': ('collapse',)
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            if obj.section_type == 'hero':
                return HeroSectionForm
            elif obj.section_type == 'mission':
                return MissionSectionForm
            elif obj.section_type == 'values':
                return ValuesSectionForm
            elif obj.section_type == 'team':
                return TeamSectionForm
            elif obj.section_type == 'history':
                return HistorySectionForm
            elif obj.section_type == 'achievements':
                return AchievementsSectionForm
        return super().get_form(request, obj, **kwargs)

    def get_inlines(self, request, obj=None):
        if obj and obj.section_type == 'stats':
            return [StatInline]
        return []

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        obj = self.get_object(request, object_id)
        if obj and obj.section_type == 'team':
            extra_context['show_team_edit_link'] = True
            extra_context['team_edit_url'] = reverse('core:team_section_edit')
        return super().change_view(request, object_id, form_url, extra_context=extra_context)


from .forms import StatAdminForm


class StatAdmin(admin.ModelAdmin):
    list_display = ('title', 'number', 'section', 'order', 'is_active')
    list_filter = ('section', 'is_active')
    search_fields = ('title', 'description', 'number')
    list_editable = ('order', 'is_active')
    form = StatAdminForm
    form = StatAdminForm


class QuickLinkInline(admin.TabularInline):
    model = QuickLink
    extra = 1
    fields = ('name', 'url', 'order')



class FooterAdmin(admin.ModelAdmin):
    form = FooterForm
    list_display = ('email', 'phone_number', 'created_at', 'updated_at')
    search_fields = ('email', 'phone_number', 'address', 'copyright_text')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [QuickLinkInline]
    fieldsets = (
        (None, {
            'fields': ('logo', 'description', 'copyright_text'),
        }),
        ('Contact Information', {
            'fields': ('address', 'phone_number', 'email'),
        }),
        ('Social Media Links', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url', 'youtube_url'),
        }),
    )








class PopupAdmin(admin.ModelAdmin):
    list_display = ('heading', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('heading', 'text')
    list_editable = ('is_active',)


admin.site.register(HeroSlide, HeroSlideAdmin)
admin.site.register(WebsiteTheme, WebsiteThemeAdmin)
admin.site.register(AboutSection, AboutSectionAdmin)
admin.site.register(Stat, StatAdmin)
admin.site.register(Footer, FooterAdmin)
