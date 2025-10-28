from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Team, Player
from django.db.models import Count, Q


class TeamListView(ListView):
    model = Team
    template_name = 'teams/team_list.html'
    context_object_name = 'teams'
    paginate_by = 12
    
    def get_queryset(self):
        # Annotate active players count to avoid per-template DB hits and unsupported template calls
        return Team.objects.filter(is_active=True).annotate(
            active_players=Count('players', filter=Q(players__is_active=True))
        ).order_by('name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add PageHero for teams page
        try:
            from core.models import PageHero
            context['page_hero'] = PageHero.objects.get(page='teams', is_active=True)
        except PageHero.DoesNotExist:
            context['page_hero'] = None
        # Add AboutSection (team) so templates can show contact info
        try:
            from core.models import AboutSection
            context['team_section'] = AboutSection.objects.filter(section_type='team', is_active=True).first()
        except Exception:
            context['team_section'] = None
        return context


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