from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.utils import timezone
from .models import Event
from core.models import PageHero


class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 9

    def get_queryset(self):
        # Show all events ordered by date (most recent first)
        # This ensures admin changes are immediately visible
        return Event.objects.all().order_by('-date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add PageHero for events page
        try:
            context['page_hero'] = PageHero.objects.get(page='events', is_active=True)
        except PageHero.DoesNotExist:
            context['page_hero'] = None
        return context


class UpcomingEventsView(ListView):
    model = Event
    template_name = 'events/upcoming_events.html'
    context_object_name = 'events'
    paginate_by = 9

    def get_queryset(self):
        today = timezone.now().date()
        return Event.objects.filter(date__gte=today).order_by('date')


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add all event images to the context
        context['event_images'] = self.object.images.all()
        return context