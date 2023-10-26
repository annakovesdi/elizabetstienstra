from django.db import models
from ckeditor.fields import RichTextField


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=60)
    friendly_name = models.CharField(max_length=60, null=True, blank=True)
    description = RichTextField(null=True, blank=True)

    def __str__(self):
        return str(self.name)

    def get_friendly_name(self):
        return self.friendly_name


class Work(models.Model):
    category = models.ForeignKey(
        'Category', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='category')
    title = models.CharField(max_length=254)
    date = models.CharField(max_length=10)
    size = models.CharField(max_length=100)
    materials = models.CharField(max_length=254)
    description = RichTextField(null=True, blank=True)
    image = models.ImageField(null=False, blank=False)
    image2 = models.ImageField(null=True, blank=True)
    image3 = models.ImageField(null=True, blank=True)
    image4 = models.ImageField(null=True, blank=True)
    image5 = models.ImageField(null=True, blank=True)
    image6 = models.ImageField(null=True, blank=True)
    image7 = models.ImageField(null=True, blank=True)
    image8 = models.ImageField(null=True, blank=True)
    image9 = models.ImageField(null=True, blank=True)
    image10 = models.ImageField(null=True, blank=True)
    image11 = models.ImageField(null=True, blank=True)
    image12 = models.ImageField(null=True, blank=True)
    image13 = models.ImageField(null=True, blank=True)
    image14 = models.ImageField(null=True, blank=True)
    image15 = models.ImageField(null=True, blank=True)
    image16 = models.ImageField(null=True, blank=True)
    image17 = models.ImageField(null=True, blank=True)
    image18 = models.ImageField(null=True, blank=True)
    image19 = models.ImageField(null=True, blank=True)
    image20 = models.ImageField(null=True, blank=True)
    image21 = models.ImageField(null=True, blank=True)
    image22 = models.ImageField(null=True, blank=True)
    image23 = models.ImageField(null=True, blank=True)
    image24 = models.ImageField(null=True, blank=True)
    image25 = models.ImageField(null=True, blank=True)
    image26 = models.ImageField(null=True, blank=True)
    image27 = models.ImageField(null=True, blank=True)
    image28 = models.ImageField(null=True, blank=True)
    image29 = models.ImageField(null=True, blank=True)
    image30 = models.ImageField(null=True, blank=True)
    hide = models.BooleanField(default=False)
    courtesy_of_gallery = models.BooleanField(default=False)
    url = models.CharField(null=True, blank=True, max_length=1000)

    def __str__(self):
        return str(self.title)