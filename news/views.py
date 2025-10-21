from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import NewsArticle


class NewsListView(ListView):
    model = NewsArticle
    template_name = 'news/news_list.html'
    context_object_name = 'articles'
    paginate_by = 9
    
    def get_queryset(self):
        return NewsArticle.objects.filter(is_published=True).order_by('-published_date')


class NewsDetailView(DetailView):
    model = NewsArticle
    template_name = 'news/news_detail.html'
    context_object_name = 'article'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'