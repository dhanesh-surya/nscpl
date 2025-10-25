from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Event


class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 9
    
    def get_queryset(self):
        return Event.objects.filter(is_upcoming=True).order_by('date')


class UpcomingEventsView(ListView):
    model = Event
    template_name = 'events/upcoming_events.html'
    context_object_name = 'events'
    paginate_by = 9
    
    def get_queryset(self):
        return Event.objects.filter(is_upcoming=True).order_by('date')


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'