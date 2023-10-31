from django.db import models


class Home(models.Model):
    image = models.ImageField(null=False, blank=False)
    name = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return str(self.title)