from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('theme-customize/', views.ThemeCustomizeView.as_view(), name='theme_customize'),
    path('theme-preview/', views.ThemePreviewView.as_view(), name='theme_preview'),
    path('hero-section-edit/', views.HeroSectionEditView.as_view(), name='hero_section_edit'),
    path('mission-section-edit/', views.MissionSectionEditView.as_view(), name='mission_section_edit'),
    path('values-section-edit/', views.ValuesSectionEditView.as_view(), name='values_section_edit'),
    path('team-section-edit/', views.TeamSectionEditView.as_view(), name='team_section_edit'),
    path('history-section-edit/', views.HistorySectionEditView.as_view(), name='history_section_edit'),
    path('achievements-section-edit/', views.AchievementsSectionEditView.as_view(), name='achievements_section_edit'),
    path('footer-edit/<int:pk>/change/', views.FooterEditView.as_view(), name='footer_edit'),
    path('team-member/add/', views.AboutTeamMemberCreateView.as_view(), name='add_team_member'),
    path('team-member/<int:pk>/edit/', views.AboutTeamMemberUpdateView.as_view(), name='edit_team_member'),
    path('team-member/<int:pk>/delete/', views.AboutTeamMemberDeleteView.as_view(), name='delete_team_member'),
    path('page/<slug:slug>/', views.PageDetailView.as_view(), name='page_detail'),
]