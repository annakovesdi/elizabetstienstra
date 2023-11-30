from django.db import models
from ckeditor.fields import RichTextField


class Home(models.Model):
    image = models.ImageField(null=False, blank=False)
    name = models.CharField(max_length=500, null=True, blank=True)
    text = RichTextField(null=True, blank=True)
    url = models.CharField(max_length=500, null=True, blank=True)
    urltext = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return str(self.title)