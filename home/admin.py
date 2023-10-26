from django.contrib import admin
from .models import Home


class HomeAdmin(admin.ModelAdmin):
    list_display = (
        'image',
    )


admin.site.register(Home, HomeAdmin)