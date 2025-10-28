from django import forms
from django.utils.text import slugify
from .models import Popup


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


class PopupForm(forms.ModelForm):
    class Meta:
        model = Popup
        fields = ['heading', 'text', 'image', 'is_active', 'background_color', 'text_color']
        widgets = {
            'heading': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'background_color': ColorPickerWidget(),
            'text_color': ColorPickerWidget(),
        }
from .models import (
    WebsiteTheme, AboutSection, Footer, QuickLink,
    Stat, Value, AboutTeamMember
)
from .models import RecognitionAchievement
from django.forms import inlineformset_factory



# Placeholder forms to satisfy admin.py imports
class StatForm(forms.ModelForm):
    class Meta:
        model = Stat
        fields = '__all__'

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
        }

class AboutSectionForm(forms.ModelForm):
    class Meta:
        model = AboutSection
        fields = '__all__'
        widgets = {
            'background_color': ColorPickerWidget(),
            'text_color': ColorPickerWidget(),
            'section_background_color': ColorPickerWidget(),
            'section_background_overlay': ColorPickerWidget(),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@example.com'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 555 555 5555'}),
            'contact_linkedin': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://www.linkedin.com/in/username/'}),
            'contact_twitter': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://twitter.com/username'}),
        }

class HeroSectionForm(forms.ModelForm):
    class Meta:
        model = AboutSection
        fields = '__all__'
        widgets = {
            'background_color': ColorPickerWidget(),
            'text_color': ColorPickerWidget(),
            'section_background_color': ColorPickerWidget(),
            'section_background_overlay': ColorPickerWidget(),
        }

class MissionSectionForm(forms.ModelForm):
    class Meta:
        model = AboutSection
        fields = '__all__'
        widgets = {
            'background_color': ColorPickerWidget(),
            'text_color': ColorPickerWidget(),
            'section_background_color': ColorPickerWidget(),
            'section_background_overlay': ColorPickerWidget(),
        }

class ValuesSectionForm(forms.ModelForm):
    class Meta:
        model = AboutSection
        fields = '__all__'
        widgets = {
            'background_color': ColorPickerWidget(),
            'text_color': ColorPickerWidget(),
            'section_background_color': ColorPickerWidget(),
            'section_background_overlay': ColorPickerWidget(),
        }

class TeamSectionForm(forms.ModelForm):
    class Meta:
        model = AboutSection
        fields = '__all__'
        widgets = {
            'background_color': ColorPickerWidget(),
            'text_color': ColorPickerWidget(),
            'section_background_color': ColorPickerWidget(),
            'section_background_overlay': ColorPickerWidget(),
        }

class HistorySectionForm(forms.ModelForm):
    class Meta:
        model = AboutSection
        fields = '__all__'
        widgets = {
            'background_color': ColorPickerWidget(),
            'text_color': ColorPickerWidget(),
            'section_background_color': ColorPickerWidget(),
            'section_background_overlay': ColorPickerWidget(),
        }

class AchievementsSectionForm(forms.ModelForm):
    class Meta:
        model = AboutSection
        fields = '__all__'
        widgets = {
            'background_color': ColorPickerWidget(),
            'text_color': ColorPickerWidget(),
            'section_background_color': ColorPickerWidget(),
            'section_background_overlay': ColorPickerWidget(),
        }

class AboutTeamMemberForm(forms.ModelForm):
    class Meta:
        model = AboutTeamMember
        fields = '__all__'
        widgets = {
            'team': forms.Select(attrs={'class': 'form-select'}),
            'background_color': ColorPickerWidget(),
            'background_gradient': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'e.g., linear-gradient(45deg, #ff0000, #0000ff)'}),
            'background_overlay': ColorPickerWidget(),
            'background_overlay_opacity': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '1', 'step': '0.1'}),
            'animation_type': forms.Select(attrs={'class': 'form-select'}),
        }



class FooterForm(forms.ModelForm):
    class Meta:
        model = Footer
        fields = ('logo', 'description', 'copyright_text', 'address', 'phone_number', 'email', 'facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url', 'youtube_url')

QuickLinkFormSet = inlineformset_factory(Footer, QuickLink, fields=('name', 'url', 'order'), extra=1, can_delete=True)


# A list of Font Awesome icons (you can expand this list)
FONT_AWESOME_ICONS = [
    ('fa-solid fa-star', 'Star'),
    ('fa-solid fa-heart', 'Heart'),
    ('fa-solid fa-check', 'Check'),
    ('fa-solid fa-xmark', 'Times'),
    ('fa-solid fa-gear', 'Gear'),
    ('fa-solid fa-house', 'Home'),
    ('fa-solid fa-user', 'User'),
    ('fa-solid fa-envelope', 'Envelope'),
    ('fa-solid fa-phone', 'Phone'),
    ('fa-solid fa-location-dot', 'Location'),
    ('fa-solid fa-calendar', 'Calendar'),
    ('fa-solid fa-clock', 'Clock'),
    ('fa-solid fa-image', 'Image'),
    ('fa-solid fa-file', 'File'),
    ('fa-solid fa-folder', 'Folder'),
    ('fa-solid fa-chart-simple', 'Chart Simple'),
    ('fa-solid fa-globe', 'Globe'),
    ('fa-solid fa-lightbulb', 'Lightbulb'),
    ('fa-solid fa-trophy', 'Trophy'),
    ('fa-solid fa-award', 'Award'),
    ('fa-solid fa-handshake', 'Handshake'),
    ('fa-solid fa-users', 'Users'),
    ('fa-solid fa-briefcase', 'Briefcase'),
    ('fa-solid fa-building', 'Building'),
    ('fa-solid fa-dollar-sign', 'Dollar Sign'),
    ('fa-solid fa-percent', 'Percent'),
    ('fa-solid fa-code', 'Code'),
    ('fa-solid fa-terminal', 'Terminal'),
    ('fa-solid fa-cloud', 'Cloud'),
    ('fa-solid fa-sun', 'Sun'),
    ('fa-solid fa-moon', 'Moon'),
    ('fa-solid fa-bell', 'Bell'),
    ('fa-solid fa-bookmark', 'Bookmark'),
    ('fa-solid fa-camera', 'Camera'),
    ('fa-solid fa-cart-shopping', 'Shopping Cart'),
    ('fa-solid fa-comment', 'Comment'),
    ('fa-solid fa-compass', 'Compass'),
    ('fa-solid fa-copy', 'Copy'),
    ('fa-solid fa-credit-card', 'Credit Card'),
    ('fa-solid fa-database', 'Database'),
    ('fa-solid fa-desktop', 'Desktop'),
    ('fa-solid fa-download', 'Download'),
    ('fa-solid fa-edit', 'Edit'),
    ('fa-solid fa-exclamation-triangle', 'Exclamation Triangle'),
    ('fa-solid fa-eye', 'Eye'),
    ('fa-solid fa-filter', 'Filter'),
    ('fa-solid fa-flag', 'Flag'),
    ('fa-solid fa-gift', 'Gift'),
    ('fa-solid fa-graduation-cap', 'Graduation Cap'),
    ('fa-solid fa-hashtag', 'Hashtag'),
    ('fa-solid fa-info-circle', 'Info Circle'),
    ('fa-solid fa-key', 'Key'),
    ('fa-solid fa-laptop', 'Laptop'),
    ('fa-solid fa-link', 'Link'),
    ('fa-solid fa-lock', 'Lock'),
    ('fa-solid fa-magnifying-glass', 'Magnifying Glass'),
    ('fa-solid fa-map-marker-alt', 'Map Marker Alt'),
    ('fa-solid fa-microphone', 'Microphone'),
    ('fa-solid fa-mobile-alt', 'Mobile Alt'),
    ('fa-solid fa-music', 'Music'),
    ('fa-solid fa-paper-plane', 'Paper Plane'),
    ('fa-solid fa-pencil-alt', 'Pencil Alt'),
    ('fa-solid fa-play', 'Play'),
    ('fa-solid fa-print', 'Print'),
    ('fa-solid fa-question-circle', 'Question Circle'),
    ('fa-solid fa-redo', 'Redo'),
    ('fa-solid fa-refresh', 'Refresh'),
    ('fa-solid fa-reply', 'Reply'),
    ('fa-solid fa-rss', 'RSS'),
    ('fa-solid fa-save', 'Save'),
    ('fa-solid fa-share-alt', 'Share Alt'),
    ('fa-solid fa-shopping-bag', 'Shopping Bag'),
    ('fa-solid fa-shopping-cart', 'Shopping Cart'),
    ('fa-solid fa-sign-in-alt', 'Sign In Alt'),
    ('fa-solid fa-sign-out-alt', 'Sign Out Alt'),
    ('fa-solid fa-sitemap', 'Sitemap'),
    ('fa-solid fa-sliders-h', 'Sliders H'),
    ('fa-solid fa-smile', 'Smile'),
    ('fa-solid fa-sort', 'Sort'),
    ('fa-solid fa-spinner', 'Spinner'),
    ('fa-solid fa-square', 'Square'),
    ('fa-solid fa-stream', 'Stream'),
    ('fa-solid fa-sync', 'Sync'),
    ('fa-solid fa-tag', 'Tag'),
    ('fa-solid fa-th', 'Th'),
    ('fa-solid fa-thumbs-up', 'Thumbs Up'),
    ('fa-solid fa-ticket-alt', 'Ticket Alt'),
    ('fa-solid fa-times', 'Times'),
    ('fa-solid fa-trash', 'Trash'),
    ('fa-solid fa-undo', 'Undo'),
    ('fa-solid fa-upload', 'Upload'),
    ('fa-solid fa-video', 'Video'),
    ('fa-solid fa-wallet', 'Wallet'),
    ('fa-solid fa-wifi', 'Wifi'),
    ('fa-solid fa-wrench', 'Wrench'),
]

class IconSelectWidget(forms.Select):
    def __init__(self, attrs=None, choices=()):
        super().__init__(attrs, choices=FONT_AWESOME_ICONS)

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        if value:
            option['attrs']['data-icon'] = value
            option['attrs']['class'] = 'fa-icon-option'
        return option

    class Media:
        css = {
            'all': ('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css',)
        }
        js = ('https://code.jquery.com/jquery-3.6.0.min.js', 'core/js/icon_select.js',)


class StatAdminForm(forms.ModelForm):
    icon = forms.ChoiceField(choices=FONT_AWESOME_ICONS, widget=IconSelectWidget)

    class Meta:
        model = Stat
        fields = '__all__'


class ValueForm(forms.ModelForm):
    icon = forms.ChoiceField(choices=FONT_AWESOME_ICONS, widget=IconSelectWidget, required=False)
    
    class Meta:
        model = Value
        fields = '__all__'
        widgets = {
            'color': ColorPickerWidget(),
            'background_color': ColorPickerWidget(),
            'background_overlay': ColorPickerWidget(),
        }

class RecognitionAchievementForm(forms.ModelForm):
    class Meta:
        model = RecognitionAchievement
        fields = ['title', 'description', 'image', 'icon', 'url', 'is_clickable']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "e.g. 'fas fa-trophy'"}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'is_clickable': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


from page_content.models import BlockType, Page, Block, MenuItem, StyleOptions
from django.forms.models import inlineformset_factory


class BlockForm(forms.ModelForm):
    class Meta:
        model = Block
        fields = ['block_type', 'title', 'content', 'order', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width:80px;'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


BlockInlineFormSet = inlineformset_factory(Page, Block, form=BlockForm, extra=0, can_delete=True)


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['title', 'slug', 'intro', 'content', 'is_published', 'template_name']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'intro': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'template_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if slug:
            return slugify(slug)
        return slug


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['title', 'slug', 'parent', 'page', 'url', 'order', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'parent': forms.Select(attrs={'class': 'form-select'}),
            'page': forms.Select(attrs={'class': 'form-select'}),
            'url': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width:80px;'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if slug:
            return slugify(slug)
        return slug


class StyleOptionsForm(forms.ModelForm):
    class Meta:
        model = StyleOptions
        fields = '__all__'
        widgets = {
            'background_type': forms.Select(attrs={'class': 'form-select'}),
            'background_color': ColorPickerWidget(),
            'background_gradient': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'e.g., linear-gradient(45deg, #ff0000, #0000ff)'}),
            'text_color': ColorPickerWidget(),
            'background_image': forms.FileInput(attrs={'class': 'form-control'}),
            'background_image_opacity': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '1', 'step': '0.1'}),
            'text_align': forms.Select(attrs={'class': 'form-select'}),
            'padding_top': forms.Select(attrs={'class': 'form-select'}),
            'padding_bottom': forms.Select(attrs={'class': 'form-select'}),
            'padding_left': forms.Select(attrs={'class': 'form-select'}),
            'padding_right': forms.Select(attrs={'class': 'form-select'}),
            'margin_top': forms.Select(attrs={'class': 'form-select'}),
            'margin_bottom': forms.Select(attrs={'class': 'form-select'}),
            'container_width': forms.Select(attrs={'class': 'form-select'}),
            'border_radius': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '50'}),
            'shadow': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'animate_on_scroll': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hover_effect': forms.Select(attrs={'class': 'form-select'}),
            'custom_class': forms.TextInput(attrs={'class': 'form-control'}),
        }
