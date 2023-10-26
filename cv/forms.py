from django import forms
from .models import Cv


class CvForm(forms.ModelForm):
    ''' Cv Form with all fields '''
    class Meta:
        model = Cv
        fields = '__all__'