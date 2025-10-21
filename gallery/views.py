from django.shortcuts import render
from django.views.generic import ListView
from .models import GalleryItem, Category


class GalleryView(ListView):
    model = GalleryItem
    template_name = 'gallery/gallery.html'
    context_object_name = 'gallery_items'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = GalleryItem.objects.all().order_by('-uploaded_date')
        
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
        
        return context