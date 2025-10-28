from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.html import format_html
from .models import PlayerRegistration
from .forms import PlayerRegistrationForm
from .models import RegistrationPageSetting
from .forms import RegistrationPageSettingForm

class PlayerRegistrationAdmin(admin.ModelAdmin):
    form = PlayerRegistrationForm
    change_form_template = 'admin/registration/playerregistration/change_form.html'
from .views import generate_player_pdf

class PlayerRegistrationAdmin(admin.ModelAdmin):
    list_display = ('sur_name', 'first_name', 'email', 'phone_number', 'venue', 'date_of_event', 'approved')
    list_filter = ('approved', 'venue', 'date_of_event')
    search_fields = ('sur_name', 'first_name', 'email', 'phone_number', 'venue')
    actions = ['download_pdf', 'approve_registrations', 'disapprove_registrations']

    def download_pdf(self, request, queryset):
        if queryset.count() == 1:
            player = queryset.first()
            pdf_file = generate_player_pdf(request, player.id)
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{player.sur_name}_{player.first_name}_registration.pdf"'
            return response
        else:
            self.message_user(request, "Please select only one registration to download as PDF.")
    download_pdf.short_description = "Download selected registration as PDF"

    def approve_registrations(self, request, queryset):
        queryset.update(approved=True)
        self.message_user(request, "Selected registrations have been approved.")
    approve_registrations.short_description = "Approve selected registrations"

    def disapprove_registrations(self, request, queryset):
        queryset.update(approved=False)
        self.message_user(request, "Selected registrations have been disapproved.")
    disapprove_registrations.short_description = "Disapprove selected registrations"

admin.site.register(PlayerRegistration, PlayerRegistrationAdmin)
 
class RegistrationPageSettingAdmin(admin.ModelAdmin):
    form = RegistrationPageSettingForm
    list_display = ('name', 'is_active', 'updated_at')
    list_editable = ('is_active',)

admin.site.register(RegistrationPageSetting, RegistrationPageSettingAdmin)
