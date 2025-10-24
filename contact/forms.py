from django import forms
from .models import ContactMessage
from django_ckeditor_5.widgets import CKEditor5Widget


class ContactForm(forms.ModelForm):
    """Model form for contact message submissions"""
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Full Name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Phone Number (Optional)'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'What is this about?',
                'required': True
            }),
            'message': CKEditor5Widget(attrs={'class': 'django_ckeditor_5', 'data-field-name': 'message', 'data-config-name': 'default'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add form validation attributes
        self.fields['name'].widget.attrs.update({
            'minlength': '2',
            'maxlength': '100'
        })
        self.fields['email'].widget.attrs.update({
            'maxlength': '254'
        })
        self.fields['phone'].widget.attrs.update({
            'maxlength': '20'
        })
        self.fields['subject'].widget.attrs.update({
            'minlength': '5',
            'maxlength': '200'
        })
        self.fields['message'].widget.attrs.update({
            'minlength': '10',
            'maxlength': '2000'
        })
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            # Remove extra whitespace and ensure proper capitalization
            name = ' '.join(name.strip().split())
        return name
    
    def clean_subject(self):
        subject = self.cleaned_data.get('subject')
        if subject:
            # Remove extra whitespace
            subject = ' '.join(subject.strip().split())
        return subject
    
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if message:
            # Remove extra whitespace but preserve line breaks
            message = '\n'.join(line.strip() for line in message.strip().split('\n'))
        return message
