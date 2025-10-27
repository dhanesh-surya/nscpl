from django import forms
from .models import PlayerRegistration
from .models import RegistrationPageSetting

class PlayerRegistrationForm(forms.ModelForm):
    venue = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control custom-venue-class', 'placeholder': 'Venue'}))
    date_of_event = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

class CustomPlayerRegistrationForm(PlayerRegistrationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput) or \
               isinstance(field.widget, forms.Textarea) or \
               isinstance(field.widget, forms.Select) or \
               isinstance(field.widget, forms.EmailInput) or \
               isinstance(field.widget, forms.DateInput):
                current_classes = field.widget.attrs.get('class', '').split()
                if 'custom-form-control' not in current_classes:
                    current_classes.append('custom-form-control')
                field.widget.attrs['class'] = ' '.join(current_classes)



    class Meta:
        model = PlayerRegistration
        fields = [
            'sur_name',
            'first_name',
            'fathers_name',
            'date_of_birth',
            'gender',
            'address',
            'city',
            'state',
            'zip_code',
            'country',
            'email',
            'phone_number',
            'whatsapp_number',
            'faster_bowler',
            'spin_bowler',
            'batting_proficiency',
            'primary_playing_role',
            'secondary_playing_role',
            'physically_fit',
            'declaration_past_tournament',
            'declaration_parents_aware',
            'declaration_indemnify_organizers',
            'declaration_emergency_care',
            'declaration_photo_video_consent',
            'declaration_true_info',
            'transaction_id',
            'transaction_screenshot',
            'photo',
        ]
        widgets = {
            'sur_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'FIRST NAME'}),
            'fathers_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "FATHER'S NAME"}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact No.'}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Whatsapp No.'}),
            'faster_bowler': forms.Select(attrs={'class': 'form-control'}),
            'spin_bowler': forms.Select(attrs={'class': 'form-control'}),
            'batting_proficiency': forms.Select(attrs={'class': 'form-control'}),
            'primary_playing_role': forms.Select(attrs={'class': 'form-control'}),
            'secondary_playing_role': forms.Select(attrs={'class': 'form-control'}),
            'physically_fit': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'declaration_past_tournament': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'declaration_parents_aware': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'declaration_indemnify_organizers': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'declaration_emergency_care': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'declaration_photo_video_consent': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'declaration_true_info': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'transaction_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Transaction ID'}),
            'transaction_screenshot': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'sur_name': 'Last Name',
            'first_name': 'First Name',
            'fathers_name': "Father's Name",
            'date_of_birth': 'Date of Birth',
            'contact_no': 'Contact Number',
            'whatsapp_no': 'WhatsApp Number',
            'faster_bowler': 'Faster Bowler Type',
            'spin_bowler': 'Spin Bowler Type',
            'right_hand_batter': 'Right Hand Batter',
            'left_hand_batter': 'Left Hand Batter',
            'playing_role': 'Playing Role',
            'declaration_past_tournament': 'I hereby declare that I have not played in any of the hard ball cricket tournament in the past.',
            'declaration_parents_aware': 'I hereby declare that my parents are aware of my participation in the trial and have no objection of whatsoever. I have informed my parents about the rules / terms and condition of the event and that they indorse my signing of this declaration on there behalf as well.',
            'declaration_indemnify_organizers': 'I hereby indemnify the organizers ( and all associated of the organizers ) from any casualty / mishap/any loss to me / my property during the process of attending the trials.',
            'declaration_emergency_care': 'I hereby give my consent for emergency medical care prescribed by authorized doctor and that this care may be giving under whatever condition are necessary to preserve the my life our well-being .the costs shall be come by me /my family.',
            'declaration_photo_video_consent': 'I hereby give my consent to the organizer to take photographs video recording and / or sound recording of my participation in documenting the activities.',
            'declaration_true_info': 'I hereby declare that all the details given above in the registration form are true and correct to the best of my knowledge and belief . In the event of any information being found false or incorrect or myself being found not eligible in terms of eligibility criteria for the participation . My name is liable to be cancelled without any notice.',
            'transaction_id': 'Transaction ID',
            'transaction_screenshot': 'Transaction Screenshot',
        }


class RegistrationPageSettingForm(forms.ModelForm):
    class Meta:
        model = RegistrationPageSetting
        fields = [
            'name', 'is_active', 'primary_color', 'accent_color', 'background_color', 'text_color',
            'heading_color', 'subtitle_color',
            'button_primary_bg', 'button_primary_text', 'card_background', 'card_border_color', 'card_border_radius',
            'font_family', 'font_size_base', 'custom_css'
        ]
        widgets = {
            'primary_color': forms.TextInput(attrs={'type': 'color'}),
            'accent_color': forms.TextInput(attrs={'type': 'color'}),
            'background_color': forms.TextInput(attrs={'type': 'color'}),
            'text_color': forms.TextInput(attrs={'type': 'color'}),
            'heading_color': forms.TextInput(attrs={'type': 'color'}),
            'subtitle_color': forms.TextInput(attrs={'type': 'color'}),
            'button_primary_bg': forms.TextInput(attrs={'type': 'color'}),
            'button_primary_text': forms.TextInput(attrs={'type': 'color'}),
            'card_background': forms.TextInput(attrs={'type': 'color'}),
            'card_border_color': forms.TextInput(attrs={'type': 'color'}),
        }