from django import forms
from .models import About


class AboutForm(forms.ModelForm):
    ''' About editing form '''
    class Meta:
        model = About
        fields = '__all__'