from django.shortcuts import render
from django.views.generic import ListView
from .models import GalleryItem, Category


class GalleryView(ListView):
    model = GalleryItem
    template_name = 'gallery/gallery.html'
    context_object_name = 'gallery_items'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = GalleryItem.objects.filter(video_url__isnull=True).order_by('-uploaded_date')
        
        # Filter by category if specified
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Filter by tag if specified
        tag = self.request.GET.get('tag')
        if tag:
            queryset = queryset.filter(tags__icontains=tag)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True).order_by('name')
        
        # Get all unique tags
        all_items = GalleryItem.objects.all()
        all_tags = set()
        for item in all_items:
            all_tags.update(item.tag_list)
        context['all_tags'] = sorted(list(all_tags))
        # Video items (separate)
        video_qs = GalleryItem.objects.filter(video_url__isnull=False).order_by('-uploaded_date')
        video_items = []
        import re
        for v in video_qs:
            thumb = v.youtube_thumbnail()
            # extract video id
            vid = None
            patterns = [
                r'(?:youtube\.com\/(?:[^\/\n\s]+\/\s*)*(?:v\/|e\/|watch\?.*v=|\&v=)|youtu\.be\/)([A-Za-z0-9_-]{11})',
                r'(?:youtube\.com\/embed\/)([A-Za-z0-9_-]{11})',
                r'(?:youtube\.com\/shorts\/)([A-Za-z0-9_-]{11})'
            ]
            for p in patterns:
                m = re.search(p, v.video_url)
                if m:
                    vid = m.group(1)
                    break
            video_items.append({
                'title': v.title,
                'category': v.category,
                'video_url': v.video_url,
                'youtube_thumbnail': thumb,
                'video_id': vid,
            })
        context['video_items'] = video_items
        
        # Add PageHero for gallery page
        try:
            from core.models import PageHero
            context['page_hero'] = PageHero.objects.get(page='gallery', is_active=True)
        except PageHero.DoesNotExist:
            context['page_hero'] = None
        
        return context