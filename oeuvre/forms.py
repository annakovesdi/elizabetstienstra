from django import forms
from .models import Work, Category, Image


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ImageForm(forms.Form):
    images = MultipleFileField()


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


