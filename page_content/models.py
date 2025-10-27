from django.db import models
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class BlockType(models.Model):
    """Defines types of blocks that can be attached to pages (e.g., hero, gallery, faq).
    Some block types can be marked compulsory so every new page will get them by default.
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    is_compulsory = models.BooleanField(default=False, help_text="If true, this block will be auto-created when a page is saved")

    class Meta:
        verbose_name = 'Block Type'
        verbose_name_plural = 'Block Types'

    def __str__(self):
        return self.name


class StyleOptionsMixin(models.Model):
    """Mixin to add style_options to block models"""
    style_options = models.OneToOneField('StyleOptions', on_delete=models.SET_NULL, null=True, blank=True, help_text='Custom styling options for this block')

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Auto-create StyleOptions if not exists
        if not self.style_options:
            self.style_options = StyleOptions.objects.create()
        super().save(*args, **kwargs)


class StyleOptions(models.Model):
    """Reusable styling options for content blocks"""

    # Background Options
    BACKGROUND_TYPE_CHOICES = [
        ('color', 'Solid Color'),
        ('gradient', 'Gradient'),
        ('image', 'Image'),
    ]
    background_type = models.CharField(
        max_length=10,
        choices=BACKGROUND_TYPE_CHOICES,
        default='color',
        help_text='Type of background to use'
    )
    background_color = models.CharField(max_length=7, default='#FFFFFF', help_text='Background color (hex code)')
    background_gradient = models.TextField(blank=True, help_text='CSS gradient value (e.g., linear-gradient(45deg, #ff0000, #0000ff))')
    background_image = models.ImageField(upload_to='backgrounds/', blank=True, null=True, help_text='Background image')
    background_image_opacity = models.FloatField(default=1.0, help_text='Background image opacity (0.0-1.0)')

    # Text Options
    text_color = models.CharField(max_length=7, default='#212529', help_text='Text color (hex code)')
    text_align = models.CharField(
        max_length=10,
        choices=[
            ('left', 'Left'),
            ('center', 'Center'),
            ('right', 'Right'),
            ('justify', 'Justify')
        ],
        default='left',
        help_text='Text alignment'
    )

    # Padding/Margin Options
    PADDING_CHOICES = [
        ('none', 'None (0px)'),
        ('small', 'Small (20px)'),
        ('medium', 'Medium (40px)'),
        ('large', 'Large (80px)'),
        ('xl', 'Extra Large (120px)')
    ]

    padding_top = models.CharField(max_length=10, choices=PADDING_CHOICES, default='medium', help_text='Top padding')
    padding_bottom = models.CharField(max_length=10, choices=PADDING_CHOICES, default='medium', help_text='Bottom padding')
    padding_left = models.CharField(max_length=10, choices=PADDING_CHOICES, default='none', help_text='Left padding')
    padding_right = models.CharField(max_length=10, choices=PADDING_CHOICES, default='none', help_text='Right padding')

    margin_top = models.CharField(max_length=10, choices=PADDING_CHOICES, default='none', help_text='Top margin')
    margin_bottom = models.CharField(max_length=10, choices=PADDING_CHOICES, default='none', help_text='Bottom margin')

    # Layout Options
    container_width = models.CharField(
        max_length=10,
        choices=[
            ('full', 'Full Width'),
            ('boxed', 'Boxed'),
            ('narrow', 'Narrow')
        ],
        default='boxed',
        help_text='Container width'
    )

    border_radius = models.PositiveIntegerField(default=8, help_text='Border radius in pixels (0-50)')
    shadow = models.BooleanField(default=False, help_text='Add shadow effect')

    # Animation Options
    animate_on_scroll = models.BooleanField(default=True, help_text='Enable scroll animations')
    hover_effect = models.CharField(
        max_length=20,
        choices=[
            ('none', 'No Effect'),
            ('lift', 'Lift Up'),
            ('zoom', 'Zoom In'),
            ('fade', 'Fade'),
            ('glow', 'Glow')
        ],
        default='none',
        help_text='Hover effect for the block'
    )

    # Custom Options
    custom_class = models.CharField(max_length=200, blank=True, help_text='Additional CSS classes')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Style Options'
        verbose_name_plural = 'Style Options'

    def __str__(self):
        return f"Style Options ({self.pk})"

    def get_padding_values(self):
        """Convert padding choices to pixel values"""
        padding_map = {
            'none': '0',
            'small': '20px',
            'medium': '40px',
            'large': '80px',
            'xl': '120px'
        }
        return {
            'top': padding_map.get(self.padding_top, '40px'),
            'bottom': padding_map.get(self.padding_bottom, '40px'),
            'left': padding_map.get(self.padding_left, '0'),
            'right': padding_map.get(self.padding_right, '0')
        }

    def get_margin_values(self):
        """Convert margin choices to pixel values"""
        margin_map = {
            'none': '0',
            'small': '20px',
            'medium': '40px',
            'large': '80px',
            'xl': '120px'
        }
        return {
            'top': margin_map.get(self.margin_top, '0'),
            'bottom': margin_map.get(self.margin_bottom, '0')
        }

    def get_container_class(self):
        """Get Bootstrap container class based on width choice"""
        if self.container_width == 'full':
            return 'container-fluid'
        elif self.container_width == 'narrow':
            return 'container-narrow'
        else:  # boxed
            return 'container'

    def get_inline_styles(self):
        """Generate inline styles for the block"""
        styles = []

        # Background
        if self.background_type == 'color' and self.background_color:
            styles.append(f"background-color: {self.background_color}")
        elif self.background_type == 'gradient' and self.background_gradient:
            styles.append(f"background: {self.background_gradient}")
        elif self.background_type == 'image' and self.background_image:
            styles.append(f"background-image: url('{self.background_image.url}')")
            styles.append("background-size: cover")
            styles.append("background-position: center")
            styles.append("background-repeat: no-repeat")
            if self.background_color:
                styles.append(f"background-color: {self.background_color}")
            # Apply background image opacity
            if self.background_image_opacity < 1.0:
                styles.append(f"opacity: {self.background_image_opacity}")

        # Text color
        if self.text_color:
            styles.append(f"color: {self.text_color}")

        # Text align
        if self.text_align:
            styles.append(f"text-align: {self.text_align}")

        # Padding
        padding = self.get_padding_values()
        if padding['top'] != '40px':  # Only add if not default
            styles.append(f"padding-top: {padding['top']}")
        if padding['bottom'] != '40px':  # Only add if not default
            styles.append(f"padding-bottom: {padding['bottom']}")
        if padding['left'] != '0':  # Only add if not default
            styles.append(f"padding-left: {padding['left']}")
        if padding['right'] != '0':  # Only add if not default
            styles.append(f"padding-right: {padding['right']}")

        # Margin
        margin = self.get_margin_values()
        if margin['top'] != '0':  # Only add if not default
            styles.append(f"margin-top: {margin['top']}")
        if margin['bottom'] != '0':  # Only add if not default
            styles.append(f"margin-bottom: {margin['bottom']}")

        # Border radius
        if self.border_radius > 0:
            styles.append(f"border-radius: {self.border_radius}px")

        return '; '.join(styles)

    def get_css_classes(self):
        """Generate CSS classes for the block"""
        classes = []

        # Container width
        classes.append(self.get_container_class())

        # Shadow
        if self.shadow:
            classes.append('shadow-lg')

        # Hover effects
        if self.hover_effect == 'lift':
            classes.append('hover-lift')
        elif self.hover_effect == 'zoom':
            classes.append('hover-zoom')
        elif self.hover_effect == 'glow':
            classes.append('hover-glow')

        # Custom classes
        if self.custom_class:
            classes.extend(self.custom_class.split())

        return ' '.join(classes)


class Page(models.Model):
    """A simple CMS Page model which can hold blocks and be linked to a menu item."""
    """A simple CMS Page model which can hold blocks and be linked to a menu item."""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    intro = models.TextField(blank=True)
    content = CKEditor5Field('Content', config_name='default', blank=True)
    is_published = models.BooleanField(default=True)
    template_name = models.CharField(max_length=200, blank=True, help_text='Optional template to render this page')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # auto-generate slug if not provided
        if not self.slug:
            base = slugify(self.title)[:200]
            slug = base
            i = 1
            while Page.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug

        super().save(*args, **kwargs)

        # Ensure compulsory blocks exist for this page. This will not touch other existing sections/models.
        for bt in BlockType.objects.filter(is_compulsory=True):
            Block.objects.get_or_create(page=self, block_type=bt, defaults={'content': ''})


class Block(models.Model):
    """An instance of a block attached to a page. Content is free-form text/HTML.
    Blocks reference a BlockType so admin/UI can present the correct editor.
    """
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='blocks')
    block_type = models.ForeignKey(BlockType, on_delete=models.PROTECT, related_name='blocks')
    title = models.CharField(max_length=200, blank=True)
    content = CKEditor5Field('Block Content', config_name='default', blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Block'
        verbose_name_plural = 'Blocks'

    def __str__(self):
        return f"{self.page.title} - {self.block_type.name}"


class MenuItem(models.Model):
    """Represents an item in the site navigation. Can link to a Page or an external URL.
    Parent-child relationship allows submenus.
    """
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    page = models.ForeignKey(Page, on_delete=models.SET_NULL, null=True, blank=True, related_name='menu_items')
    url = models.CharField(max_length=255, blank=True, help_text='Optional absolute or relative URL')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = 'Menu Item'
        verbose_name_plural = 'Menu Items'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.page and self.page.slug:
            from django.urls import reverse
            try:
                return reverse('page_content:page_detail', args=[self.page.slug])
            except Exception:
                return f"/{self.page.slug}/"
        return self.url or '#'


# =====================
# Stream-like Page Blocks
# =====================

class BaseBlock(StyleOptionsMixin, models.Model):
    """Abstract base for all typed content blocks placed on a Page."""
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='content_blocks_%(class)s')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['order', 'id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @property
    def template_name(self):
        # E.g. blocks/hero_bannerblock.html -> we prefer readable filenames, so map in view
        return f"blocks/{self._meta.model_name}.html"


class HeroBannerBlock(BaseBlock):
    heading = models.CharField(max_length=200, blank=True, help_text="Optional heading for the hero section")


class HeroSlideItem(models.Model):
    block = models.ForeignKey(HeroBannerBlock, on_delete=models.CASCADE, related_name='slides')
    background_image = models.ImageField(upload_to='blocks/hero/', blank=True, null=True)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    button_text = models.CharField(max_length=50, blank=True)
    button_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.title} - {self.block.page.title}"


class TextImageBlock(BaseBlock):
    ALIGN_CHOICES = (
        ('left', 'Image Left'),
        ('right', 'Image Right'),
    )
    heading = models.CharField(max_length=200, blank=True)
    text = CKEditor5Field('Text', config_name='default', blank=True)
    image = models.ImageField(upload_to='blocks/text_image/', blank=True, null=True)
    alignment = models.CharField(max_length=5, choices=ALIGN_CHOICES, default='left')


class FeatureHighlightsBlock(BaseBlock):
    heading = models.CharField(max_length=200, blank=True)
    subheading = models.CharField(max_length=300, blank=True)


class FeatureItem(models.Model):
    block = models.ForeignKey(FeatureHighlightsBlock, on_delete=models.CASCADE, related_name='items')
    icon = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']


class TestimonialBlock(BaseBlock):
    heading = models.CharField(max_length=200, blank=True)


class TestimonialItem(models.Model):
    block = models.ForeignKey(TestimonialBlock, on_delete=models.CASCADE, related_name='testimonials')
    name = models.CharField(max_length=120)
    designation = models.CharField(max_length=120, blank=True)
    message = models.TextField()
    photo = models.ImageField(upload_to='blocks/testimonials/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']


class CallToActionBlock(BaseBlock):
    heading = models.CharField(max_length=200)
    text = models.TextField(blank=True)
    button_text = models.CharField(max_length=50, blank=True)
    button_url = models.URLField(blank=True)


class GalleryBlock(BaseBlock):
    heading = models.CharField(max_length=200, blank=True)


class GalleryImage(models.Model):
    block = models.ForeignKey(GalleryBlock, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='blocks/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']


class VideoEmbedBlock(BaseBlock):
    title = models.CharField(max_length=200, blank=True)
    embed_url = models.URLField(help_text='YouTube/Vimeo embed URL')


class FAQBlock(BaseBlock):
    heading = models.CharField(max_length=200, blank=True)


class FAQItem(models.Model):
    block = models.ForeignKey(FAQBlock, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=255)
    answer = CKEditor5Field('Answer', config_name='default')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']


class CounterStatsBlock(BaseBlock):
    heading = models.CharField(max_length=200, blank=True)


class CounterItem(models.Model):
    block = models.ForeignKey(CounterStatsBlock, on_delete=models.CASCADE, related_name='counters')
    number = models.CharField(max_length=50)
    label = models.CharField(max_length=150)
    icon = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']


class ContactFormBlock(BaseBlock):
    heading = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)


class TeamMemberBlock(BaseBlock):
    heading = models.CharField(max_length=200, blank=True)
    subheading = models.CharField(max_length=300, blank=True)


class TeamMemberItem(models.Model):
    block = models.ForeignKey(TeamMemberBlock, on_delete=models.CASCADE, related_name='members')
    photo = models.ImageField(upload_to='blocks/team/', blank=True, null=True)
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120, blank=True)
    bio = models.TextField(blank=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']


class BlogPreviewBlock(BaseBlock):
    heading = models.CharField(max_length=200, blank=True)
    count = models.PositiveIntegerField(default=3)


class TwoColumnTextBlock(BaseBlock):
    left_text = CKEditor5Field('Left Text', config_name='default', blank=True)
    right_text = CKEditor5Field('Right Text', config_name='default', blank=True)
    heading = models.CharField(max_length=200, blank=True)


class TimelineBlock(BaseBlock):
    heading = models.CharField(max_length=200, blank=True)


class TimelineStep(models.Model):
    block = models.ForeignKey(TimelineBlock, on_delete=models.CASCADE, related_name='steps')
    icon = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=150)
    detail = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']


class FooterInfoBlock(BaseBlock):
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    links_json = models.JSONField(blank=True, null=True, help_text="Optional array of links: [{name, url}]")
    copyright_text = models.CharField(max_length=255, blank=True)


class StyledContentBlock(BaseBlock):
    """A flexible content block with title and rich text content, styled with Bootstrap 5 and custom StyleOptions"""
    title = models.CharField(max_length=200, blank=True, help_text="Optional title for the content block")
    content = CKEditor5Field('Content', config_name='default', blank=True, help_text="Rich text content for the block")
