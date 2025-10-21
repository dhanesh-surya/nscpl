from django import forms
from .models import Sport

class SportForm(forms.ModelForm):
    class Meta:
        model = Sport
        fields = ['name', 'description', 'icon', 'image', 'is_active', 'rules_and_regulations', 'history']