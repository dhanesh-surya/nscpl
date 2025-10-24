from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from events.models import Event
from news.models import NewsArticle
from gallery.models import GalleryItem
from .models import HeroSlide, WebsiteTheme, AboutSection, AboutTeamMember, Value, Stat, Footer, Popup
from .forms import (
    WebsiteThemeForm, AboutSectionForm, HeroSectionForm, MissionSectionForm, 
    ValuesSectionForm, TeamSectionForm, HistorySectionForm, 
    AchievementsSectionForm, AboutTeamMemberForm, FooterForm
)
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Popup


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popup"] = Popup.objects.filter(is_active=True).first()
        context['hero_slides'] = HeroSlide.objects.filter(is_active=True).order_by('order')
        context['featured_events'] = Event.objects.filter(is_upcoming=True)[:3]
        context['latest_news'] = NewsArticle.objects.filter(is_published=True)[:3]
        context['featured_gallery'] = GalleryItem.objects.filter(is_featured=True)[:6]
        context['theme'] = WebsiteTheme.objects.filter(is_active=True).first()
        context['footer'] = Footer.objects.prefetch_related('quick_links').first()
        
        stats_section = AboutSection.objects.filter(section_type='stats', is_active=True).first()
        if stats_section:
            context['stats_section'] = stats_section
            context['stats'] = stats_section.stats.filter(is_active=True).order_by('order')
        else:
            context['stats_section'] = None
            context['stats'] = None
            
        return context


class AboutView(TemplateView):
    template_name = 'core/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['theme'] = WebsiteTheme.objects.filter(is_active=True).first()
        context['about_sections'] = AboutSection.objects.filter(is_active=True).order_by('order')
        context['team_members'] = AboutTeamMember.objects.all().order_by('order')
        context['values'] = Value.objects.filter(is_active=True).order_by('order')
        context['footer'] = Footer.objects.prefetch_related('quick_links').first()
        context['popup'] = Popup.objects.filter(is_active=True).first()
        
        return context


@method_decorator(staff_member_required, name='dispatch')
class ThemeCustomizeView(TemplateView):
    template_name = 'core/theme_customize.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        theme = WebsiteTheme.objects.filter(is_active=True).first()
        if not theme:
            theme = WebsiteTheme.objects.create(
                name="Default Theme",
                is_active=True
            )
        context['theme'] = theme
        context['form'] = WebsiteThemeForm(instance=theme)
        context['footer'] = Footer.objects.prefetch_related('quick_links').first()
        context['popup'] = Popup.objects.filter(is_active=True).first()
        return context
    
    def post(self, request, *args, **kwargs):
        theme = WebsiteTheme.objects.filter(is_active=True).first()
        if not theme:
            theme = WebsiteTheme.objects.create(
                name="Default Theme",
                is_active=True
            )
        
        form = WebsiteThemeForm(request.POST, request.FILES, instance=theme)
        if form.is_valid():
            form.save()
            messages.success(request, 'Theme updated successfully!')
            return redirect('core:theme_customize')
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, self.template_name, {'form': form, 'theme': theme})


class ThemePreviewView(TemplateView):
    template_name = 'core/theme_preview.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['theme'] = WebsiteTheme.objects.filter(is_active=True).first()
        context['footer'] = Footer.objects.prefetch_related('quick_links').first()
        context['popup'] = Popup.objects.filter(is_active=True).first()
        return context


# Specialized views for each section type
@method_decorator(staff_member_required, name='dispatch')
class HeroSectionEditView(TemplateView):
    template_name = 'core/section_forms/hero_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        section = AboutSection.objects.filter(section_type='hero').first()
        if section:
            context['form'] = HeroSectionForm(instance=section)
            context['section'] = section
        else:
            context['form'] = HeroSectionForm()
        context['footer'] = Footer.objects.prefetch_related('quick_links').first()
        context['popup'] = Popup.objects.filter(is_active=True).first()
        return context
    
    def post(self, request, *args, **kwargs):
        section = AboutSection.objects.filter(section_type='hero').first()
        form = HeroSectionForm(request.POST, request.FILES, instance=section)
        if form.is_valid():
            section = form.save(commit=False)
            section.section_type = 'hero'
            section.save()
            messages.success(request, 'Hero section updated successfully!')
            return redirect('core:hero_section_edit')
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, self.template_name, {'form': form})


@method_decorator(staff_member_required, name='dispatch')
class MissionSectionEditView(TemplateView):
    template_name = 'core/section_forms/mission_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        section = AboutSection.objects.filter(section_type='mission').first()
        if section:
            context['form'] = MissionSectionForm(instance=section)
            context['section'] = section
        else:
            context['form'] = MissionSectionForm()
        context['footer'] = Footer.objects.prefetch_related('quick_links').first()
        context['popup'] = Popup.objects.filter(is_active=True).first()
        return context
    
    def post(self, request, *args, **kwargs):
        section = AboutSection.objects.filter(section_type='mission').first()
        form = MissionSectionForm(request.POST, request.FILES, instance=section)
        if form.is_valid():
            section = form.save(commit=False)
            section.section_type = 'mission'
            section.save()
            messages.success(request, 'Mission section updated successfully!')
            return redirect('core:mission_section_edit')
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, self.template_name, {'form': form})


@method_decorator(staff_member_required, name='dispatch')
class ValuesSectionEditView(TemplateView):
    template_name = 'core/section_forms/values_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        section = AboutSection.objects.filter(section_type='values').first()
        if section:
            context['form'] = ValuesSectionForm(instance=section)
            context['section'] = section
        else:
            context['form'] = ValuesSectionForm()
        context['footer'] = Footer.objects.prefetch_related('quick_links').first()
        context['popup'] = Popup.objects.filter(is_active=True).first()
        return context
    
    def post(self, request, *args, **kwargs):
        section = AboutSection.objects.filter(section_type='values').first()
        form = ValuesSectionForm(request.POST, request.FILES, instance=section)
        if form.is_valid():
            section = form.save(commit=False)
            section.section_type = 'values'
            section.save()
            messages.success(request, 'Values section updated successfully!')
            return redirect('core:values_section_edit')
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, self.template_name, {'form': form})


@method_decorator(staff_member_required, name='dispatch')
class TeamSectionEditView(TemplateView):
    template_name = 'core/section_forms/team_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        section = AboutSection.objects.filter(section_type='team').first()
        if section:
            context['form'] = TeamSectionForm(instance=section)
            context['section'] = section
        else:
            context['form'] = TeamSectionForm()
        context['team_members'] = AboutTeamMember.objects.all().order_by('order')
        context['footer'] = Footer.objects.prefetch_related('quick_links').first()
        context['popup'] = Popup.objects.filter(is_active=True).first()
        return context
    
    def post(self, request, *args, **kwargs):
        section = AboutSection.objects.filter(section_type='team').first()
        form = TeamSectionForm(request.POST, request.FILES, instance=section)
        if form.is_valid():
            section = form.save(commit=False)
            section.section_type = 'team'
            section.save()
            messages.success(request, 'Team section updated successfully!')
            return redirect('core:team_section_edit')
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, self.template_name, {'form': form})


@method_decorator(staff_member_required, name='dispatch')
class HistorySectionEditView(TemplateView):
    template_name = 'core/section_forms/history_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        section = AboutSection.objects.filter(section_type='history').first()
        if section:
            context['form'] = HistorySectionForm(instance=section)
            context['section'] = section
        else:
            context['form'] = HistorySectionForm()
        context['footer'] = Footer.objects.prefetch_related('quick_links').first()
        context['popup'] = Popup.objects.filter(is_active=True).first()
        return context
    
    def post(self, request, *args, **kwargs):
        section = AboutSection.objects.filter(section_type='history').first()
        form = HistorySectionForm(request.POST, request.FILES, instance=section)
        if form.is_valid():
            section = form.save(commit=False)
            section.section_type = 'history'
            section.save()
            messages.success(request, 'History section updated successfully!')
            return redirect('core:history_section_edit')
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, self.template_name, {'form': form})


@method_decorator(staff_member_required, name='dispatch')
class AchievementsSectionEditView(TemplateView):
    template_name = 'core/section_forms/achievements_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        section = AboutSection.objects.filter(section_type='achievements').first()
        if section:
            context['form'] = AchievementsSectionForm(instance=section)
            context['section'] = section
        else:
            context['form'] = AchievementsSectionForm()
        context['footer'] = Footer.objects.prefetch_related('quick_links').first()
        context['popup'] = Popup.objects.filter(is_active=True).first()
        return context
    
    def post(self, request, *args, **kwargs):
        section = AboutSection.objects.filter(section_type='achievements').first()
        form = AchievementsSectionForm(request.POST, request.FILES, instance=section)
        if form.is_valid():
            section = form.save(commit=False)
            section.section_type = 'achievements'
            section.save()
            messages.success(request, 'Achievements section updated successfully!')
            return redirect('core:achievements_section_edit')
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, self.template_name, {'form': form})


    def post(self, request, *args, **kwargs):
        section = AboutSection.objects.filter(section_type='achievements').first()
        form = AchievementsSectionForm(request.POST, request.FILES, instance=section)
        if form.is_valid():
            section = form.save(commit=False)
            section.section_type = 'achievements'
            section.save()
            messages.success(request, 'Achievements section updated successfully!')
            return redirect('core:achievements_section_edit')
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, self.template_name, {'form': form})


@method_decorator(staff_member_required, name='dispatch')
class AboutTeamMemberCreateView(CreateView):
    model = AboutTeamMember
    form_class = AboutTeamMemberForm
    template_name = 'core/section_forms/team_member_form.html'
    success_url = reverse_lazy('core:team_section_edit')

    def form_valid(self, form):
        messages.success(self.request, 'Team member added successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

@method_decorator(staff_member_required, name='dispatch')
class AboutTeamMemberUpdateView(UpdateView):
    model = AboutTeamMember
    form_class = AboutTeamMemberForm
    template_name = 'core/section_forms/team_member_form.html'
    success_url = reverse_lazy('core:team_section_edit')

    def form_valid(self, form):
        messages.success(self.request, 'Team member updated successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

@method_decorator(staff_member_required, name='dispatch')
class AboutTeamMemberDeleteView(DeleteView):
    model = AboutTeamMember
    template_name = 'core/section_forms/team_member_confirm_delete.html'
    success_url = reverse_lazy('core:team_section_edit')

    def post(self, request, *args, **kwargs):
        messages.success(self.request, 'Team member deleted successfully!')
        return super().post(request, *args, **kwargs)


@method_decorator(staff_member_required, name='dispatch')
class FooterEditView(TemplateView):
    template_name = 'core/section_forms/footer_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        footer_id = kwargs.get('pk')
        if footer_id:
            footer = get_object_or_404(Footer, pk=footer_id)
        else:
            footer = Footer.objects.first()
            if not footer:
                footer = Footer.objects.create()
        context['form'] = FooterForm(instance=footer)
        context['formset'] = QuickLinkFormSet(instance=footer)
        context['footer'] = footer
        return context

    def post(self, request, *args, **kwargs):
        footer_id = kwargs.get('pk')
        if footer_id:
            footer = get_object_or_404(Footer, pk=footer_id)
        else:
            footer = Footer.objects.first()
            if not footer:
                footer = Footer.objects.create()
        form = FooterForm(request.POST, request.FILES, instance=footer)
        formset = QuickLinkFormSet(request.POST, instance=footer)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Footer section updated successfully!')
            return redirect('core:footer_edit')
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, self.template_name, {'form': form, 'formset': formset, 'footer': footer})
