from django.shortcuts import render, get_object_or_404
from .models import Page

def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug, is_published=True)
    blocks = page.blocks.filter(is_active=True).order_by('order')
    content_blocks = []
    for block in blocks:
        # Get the specific block instance
        block_model = block.block_type.slug.replace('-', '_')
        try:
            specific_block = getattr(page, f'content_blocks_{block_model}').filter(is_active=True).order_by('order').first()
            if specific_block:
                content_blocks.append(specific_block)
        except AttributeError:
            # Fallback to generic block
            content_blocks.append(block)
    
    context = {
        'page': page,
        'blocks': blocks,
        'content_blocks': content_blocks,
    }
    
    # Use custom template if specified, otherwise default
    template_name = page.template_name or 'page_content/page_detail.html'
    return render(request, template_name, context)
