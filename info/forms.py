from django import forms
from .models import Info


class InfoForm(forms.ModelForm):
    '''information form'''
    class Meta:
        model = Info
        fields = '__all__'