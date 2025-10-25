from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Team, Player


class TeamListView(ListView):
    model = Team
    template_name = 'teams/team_list.html'
    context_object_name = 'teams'
    paginate_by = 12
    
    def get_queryset(self):
        return Team.objects.filter(is_active=True).order_by('name')


class TeamDetailView(DetailView):
    model = Team
    template_name = 'teams/team_detail.html'
    context_object_name = 'team'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['players'] = Player.objects.filter(team=self.object, is_active=True).order_by('jersey_number', 'name')
        return context