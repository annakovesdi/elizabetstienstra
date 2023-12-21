from django.db import models
from ckeditor.fields import RichTextField


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=60)
    friendly_name = models.CharField(max_length=60, null=True, blank=True)

    def __str__(self):
        return str(self.name)

    def get_friendly_name(self):
        return self.friendly_name


class Work(models.Model):
    category = models.ForeignKey(
        'Category', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='category')
    title = models.CharField(max_length=254)
    date = models.DateField(verbose_name ='date, format dd-mm-yyyy')
    size = models.CharField(max_length=100)
    materials = models.CharField(max_length=254)
    description = RichTextField(null=True, blank=True)
    hide = models.BooleanField(default=False)
    courtesy_of_gallery = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ('order', '-date', )



class Image(models.Model):
    image = models.ImageField(null=True, blank=True)
    work = models.ForeignKey(Work, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.id)