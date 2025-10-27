from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView
from django.urls import reverse_lazy
from .models import Sport
from .forms import SportForm


class SportListView(ListView):
    model = Sport
    template_name = 'sports/sport_list.html'
    context_object_name = 'sports'
    
    def get_queryset(self):
        return Sport.objects.filter(is_active=True).order_by('name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add PageHero for sports page
        try:
            from core.models import PageHero
            context['page_hero'] = PageHero.objects.get(page='sports', is_active=True)
        except PageHero.DoesNotExist:
            context['page_hero'] = None
        return context


class SportDetailView(DetailView):
    model = Sport
    template_name = 'sports/sport_detail.html'
    context_object_name = 'sport'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class SportUpdateView(UpdateView):
    model = Sport
    form_class = SportForm
    template_name = 'sports/sport_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('sports:sport_list')