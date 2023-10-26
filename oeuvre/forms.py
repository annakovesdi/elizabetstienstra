from django import forms
from .models import Work, Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('description', )

    def __innit__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'description': 'Enter your description here',
        }
        for field in self.fields:
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
        self.fields[field].label = False


class WorkForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = '__all__'

    def __innit__(self, *args, **kwargs):
        super().__innit__(*args, **kwargs)
        categories = Category.objects.all()
        names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = names