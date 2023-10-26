from django.db import models
from ckeditor.fields import RichTextField


class Category(models.Model):
    ''' Cv Categories '''
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=60)
    friendly_name = models.CharField(max_length=60, default='category')

    def __str__(self):
        return str(self.name)

    def get_friendly_name(self):
        return self.friendly_name


class Cv(models.Model):
    ''' Cv Model '''
    category = models.ForeignKey(
        'Category', null=False, blank=False,
        on_delete=models.PROTECT, related_name='category')
    description = RichTextField(blank=False, null=False, default='CV items')
    hide = models.BooleanField(default=False)

    def __str__(self):
        return str(self.description)