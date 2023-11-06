from django.db import models
from ckeditor.fields import RichTextField


class About(models.Model):
    ''' About model '''
    title = models.CharField(max_length=254, null=False, blank=False)
    description = RichTextField(null=False, blank=False)
    image = models.ImageField(null=False, blank=False)
    image2 = models.ImageField(null=True, blank=True)
    image3 = models.ImageField(null=True, blank=True)
    contact = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return str(self.title)
