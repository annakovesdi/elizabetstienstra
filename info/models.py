from django.db import models
from ckeditor.fields import RichTextField
from django.utils.timezone import datetime


class Category(models.Model):
    ''' Information Categories '''
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=60)
    friendly_name = models.CharField(max_length=60)

    def __str__(self):
        return str(self.name)

    def get_friendly_name(self):
        return self.friendly_name


class Info(models.Model):
    ''' Information Model '''
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT)
    title = models.CharField(max_length=254)
    date = models.DateField(verbose_name ='date, format dd-mm-yyyy')
    description = RichTextField()
    image = models.ImageField(null=True, blank=True)
    url = models.CharField(null=True, blank=True, max_length=700)
    hide = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ('-date', )