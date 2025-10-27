from django.contrib import admin
from django import forms
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType
from .models import (
    BlockType, Page, Block, MenuItem, StyleOptions,
    HeroBannerBlock, TextImageBlock, FeatureHighlightsBlock, FeatureItem,
    TestimonialBlock, TestimonialItem, CallToActionBlock, GalleryBlock, GalleryImage,
    VideoEmbedBlock, FAQBlock, FAQItem, CounterStatsBlock, CounterItem,
    ContactFormBlock, TeamMemberBlock, TeamMemberItem, BlogPreviewBlock,
    TwoColumnTextBlock, TimelineBlock, TimelineStep, FooterInfoBlock, HeroSlideItem,
    StyledContentBlock
)
from core.forms import PageForm, StyleOptionsForm


class BlockInline(admin.StackedInline):
    model = Block
    extra = 0
    fields = ('block_type', 'title', 'content', 'order', 'is_active')
    readonly_fields = ()


class StyleOptionsAdminMixin:
    """Mixin to add style options fields to admin forms"""
    STYLE_FIELDS = [
        'background_type', 'background_color', 'background_gradient', 'background_image', 'background_image_opacity',
        'text_color', 'text_align',
        'padding_top', 'padding_bottom', 'padding_left', 'padding_right',
        'margin_top', 'margin_bottom',
        'container_width', 'border_radius', 'shadow',
        'animate_on_scroll', 'hover_effect', 'custom_class',
    ]

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(StyleOptionsAdminMixin, self).get_fieldsets(request, obj)
        # Add style options fieldset
        style_fieldset = ('Style Options', {
            'fields': tuple(f'style_{sf}' for sf in self.STYLE_FIELDS),
            'classes': ('collapse',),
        })
        # Ensure we always return a tuple for fieldsets; some parent classes
        # may return a tuple while others may return a list. Convert to tuple
        # and append our style_fieldset as a single-element tuple.
        fieldsets = tuple(fieldsets) + (style_fieldset,)
        return fieldsets

    def get_form(self, request, obj=None, **kwargs):
        # Filter out style fields from fields list if present
        if 'fields' in kwargs and kwargs['fields'] is not None:
            style_fields_to_remove = [f'style_{sf}' for sf in self.STYLE_FIELDS]
            kwargs['fields'] = [f for f in kwargs['fields'] if f not in style_fields_to_remove]
        
        # Get the base form from the parent admin class
        BaseForm = super(StyleOptionsAdminMixin, self).get_form(request, obj, **kwargs)
        
        # Create a new form class that inherits from BaseForm and adds style fields
        style_form = StyleOptionsForm()
        
        # Create form class with style fields added as class attributes with 'style_' prefix
        attrs = {}
        for name, field in style_form.fields.items():
            prefixed_name = f'style_{name}'
            attrs[prefixed_name] = field
        
        FormClass = type(f'{self.model.__name__}StyleForm', (BaseForm,), attrs)

        # Wrap __init__ to populate initial values from obj.style_options
        orig_init = getattr(FormClass, '__init__', None)

        def __init__(form_self, *fargs, **fkwargs):
            if orig_init:
                orig_init(form_self, *fargs, **fkwargs)
            # populate initial style values only if obj exists
            if obj:
                try:
                    so = getattr(obj, 'style_options', None)
                except Exception:
                    so = None
                if not so:
                    # ensure a StyleOptions exists to populate defaults
                    so = StyleOptions.objects.create()
                    obj.style_options = so
                    obj.save()
                for sf in self.STYLE_FIELDS:
                    key = f'style_{sf}'
                    if key in form_self.initial:
                        continue
                    try:
                        form_self.initial[key] = getattr(so, sf)
                    except Exception:
                        # ignore missing attrs
                        pass
            else:
                # For new objects, set defaults from StyleOptions model
                for sf in self.STYLE_FIELDS:
                    key = f'style_{sf}'
                    if key not in form_self.initial:
                        try:
                            field = StyleOptions._meta.get_field(sf)
                            if field.default is not None and not callable(field.default):
                                form_self.initial[key] = field.default
                        except Exception:
                            pass

        FormClass.__init__ = __init__
        return FormClass

    def save_model(self, request, obj, form, change):
        # First save the main object
        super().save_model(request, obj, form, change)

        # Ensure style_options exists
        so = getattr(obj, 'style_options', None)
        if not so:
            so = StyleOptions.objects.create()
            obj.style_options = so
            obj.save()

        # Pull prefixed style fields from form.cleaned_data and save to StyleOptions
        updated = False
        for sf in self.STYLE_FIELDS:
            key = f'style_{sf}'
            if key in form.cleaned_data:
                val = form.cleaned_data.get(key)
                # assign if value present (files handled by FileField)
                try:
                    setattr(so, sf, val)
                    updated = True
                except Exception:
                    # ignore invalid assignments
                    pass

        if updated:
            so.save()


class PageAdmin(admin.ModelAdmin):
    form = PageForm
    list_display = ('title', 'slug', 'is_published', 'updated_at')
    list_filter = ('is_published', 'updated_at')
    search_fields = ('title', 'slug', 'intro')
    # Sample: keep generic Block inline; typed blocks are edited in their own admin screens
    inlines = [BlockInline]
    readonly_fields = ('created_at', 'updated_at')


class BlockTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_compulsory')
    search_fields = ('name', 'slug')


# Custom form to display parent choices with nested labels (like the navbar)
class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Build flat choices showing all existing active menu items (like navbar)
        # Exclude self and descendants when editing to avoid circular parent
        exclude_pks = []
        instance = kwargs.get('instance')
        if instance and instance.pk:
            # collect descendants
            to_visit = [instance]
            while to_visit:
                cur = to_visit.pop()
                exclude_pks.append(cur.pk)
                for ch in cur.children.all():
                    to_visit.append(ch)

        base_qs = MenuItem.objects.filter(is_active=True).exclude(pk__in=exclude_pks).order_by('order', 'title')
        choices = [('', '---------')]
        choices.extend([(item.pk, item.title) for item in base_qs])

        # Replace the parent field widget choices
        self.fields['parent'].choices = choices
        # ensure correct queryset for other behaviors
        self.fields['parent'].queryset = base_qs


class MenuItemAdmin(admin.ModelAdmin):
    form = MenuItemForm
    list_display = ('title', 'parent', 'page', 'url', 'order', 'is_active')
    list_filter = ('is_active', 'parent')
    search_fields = ('title', 'url')


admin.site.register(BlockType, BlockTypeAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(MenuItem, MenuItemAdmin)


# Sample admin registrations for typed blocks
class FeatureItemInline(admin.TabularInline):
    model = FeatureItem
    extra = 0


@admin.register(FeatureHighlightsBlock)
class FeatureHighlightsBlockAdmin(StyleOptionsAdminMixin, admin.ModelAdmin):
    list_display = ('page', 'heading', 'order', 'is_active')
    list_filter = ('is_active', 'page')
    search_fields = ('heading',)
    inlines = [FeatureItemInline]


class TestimonialItemInline(admin.TabularInline):
    model = TestimonialItem
    extra = 0


@admin.register(TestimonialBlock)
class TestimonialBlockAdmin(StyleOptionsAdminMixin, admin.ModelAdmin):
    list_display = ('page', 'heading', 'order', 'is_active')
    list_filter = ('is_active', 'page')
    search_fields = ('heading',)
    inlines = [TestimonialItemInline]


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 0


class FAQItemInline(admin.TabularInline):
    model = FAQItem
    extra = 0


class CounterItemInline(admin.TabularInline):
    model = CounterItem
    extra = 0


class TeamMemberItemInline(admin.TabularInline):
    model = TeamMemberItem
    extra = 0


class HeroSlideItemInline(admin.TabularInline):
    model = HeroSlideItem
    extra = 1


class TimelineStepInline(admin.TabularInline):
    model = TimelineStep
    extra = 0


@admin.register(GalleryBlock)
class GalleryBlockAdmin(StyleOptionsAdminMixin, admin.ModelAdmin):
    list_display = ('page', 'heading', 'order', 'is_active')
    list_filter = ('is_active', 'page')
    search_fields = ('heading',)
    inlines = [GalleryImageInline]


@admin.register(FAQBlock)
class FAQBlockAdmin(StyleOptionsAdminMixin, admin.ModelAdmin):
    list_display = ('page', 'heading', 'order', 'is_active')
    list_filter = ('is_active', 'page')
    search_fields = ('heading',)
    inlines = [FAQItemInline]


@admin.register(CounterStatsBlock)
class CounterStatsBlockAdmin(StyleOptionsAdminMixin, admin.ModelAdmin):
    list_display = ('page', 'heading', 'order', 'is_active')
    list_filter = ('is_active', 'page')
    search_fields = ('heading',)
    inlines = [CounterItemInline]


@admin.register(TeamMemberBlock)
class TeamMemberBlockAdmin(StyleOptionsAdminMixin, admin.ModelAdmin):
    list_display = ('page', 'heading', 'order', 'is_active')
    list_filter = ('is_active', 'page')
    search_fields = ('heading',)
    inlines = [TeamMemberItemInline]


@admin.register(HeroBannerBlock)
class HeroBannerBlockAdmin(StyleOptionsAdminMixin, admin.ModelAdmin):
    list_display = ('page', 'heading', 'order', 'is_active')
    list_filter = ('is_active', 'page')
    search_fields = ('heading',)
    inlines = [HeroSlideItemInline]


@admin.register(TextImageBlock)
class TextImageBlockAdmin(StyleOptionsAdminMixin, admin.ModelAdmin):
    list_display = ('page', 'heading', 'alignment', 'order', 'is_active')
    list_filter = ('is_active', 'page', 'alignment')
    search_fields = ('heading',)
    inlines = []


@admin.register(CallToActionBlock)
class CallToActionBlockAdmin(StyleOptionsAdminMixin, admin.ModelAdmin):
    list_display = ('page', 'heading', 'order', 'is_active')
    list_filter = ('is_active', 'page')
    search_fields = ('heading',)
    inlines = []


@admin.register(VideoEmbedBlock)
class VideoEmbedBlockAdmin(StyleOptionsAdminMixin, admin.ModelAdmin):
    list_display = ('page', 'title', 'order', 'is_active')
    list_filter = ('is_active', 'page')
    search_fields = ('title', 'embed_url')
    inlines = []


@admin.register(ContactFormBlock)
class ContactFormBlockAdmin(StyleOptionsAdminMixin, admin.ModelAdmin):
    list_display = ('page', 'heading', 'order', 'is_active')
    list_filter = ('is_active', 'page')
    search_fields = ('heading',)
    inlines = []


@admin.register(BlogPreviewBlock)
class BlogPreviewBlockAdmin(StyleOptionsAdminMixin, admin.ModelAdmin):
    list_display = ('page', 'heading', 'count', 'order', 'is_active')
    list_filter = ('is_active', 'page')
    search_fields = ('heading',)
    inlines = []


@admin.register(TwoColumnTextBlock)
class TwoColumnTextBlockAdmin(StyleOptionsAdminMixin, admin.ModelAdmin):
    list_display = ('page', 'heading', 'order', 'is_active')
    list_filter = ('is_active', 'page')
    search_fields = ('heading',)
    inlines = []


@admin.register(TimelineBlock)
class TimelineBlockAdmin(StyleOptionsAdminMixin, admin.ModelAdmin):
    list_display = ('page', 'heading', 'order', 'is_active')
    list_filter = ('is_active', 'page')
    search_fields = ('heading',)
    inlines = [TimelineStepInline]


@admin.register(FooterInfoBlock)
class FooterInfoBlockAdmin(StyleOptionsAdminMixin, admin.ModelAdmin):
    list_display = ('page', 'phone', 'email', 'order', 'is_active')
    list_filter = ('is_active', 'page')
    search_fields = ('address', 'email', 'phone')
    inlines = []


@admin.register(StyledContentBlock)
class StyledContentBlockAdmin(StyleOptionsAdminMixin, admin.ModelAdmin):
    list_display = ('page', 'title', 'order', 'is_active')
    list_filter = ('is_active', 'page')
    search_fields = ('title', 'content')
    inlines = []
