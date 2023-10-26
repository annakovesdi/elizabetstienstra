from django.contrib import admin
from .models import About


class AboutAdmin(admin.ModelAdmin):
    list_display = (
        'title',
    )

    ordering = ('title', )


admin.site.register(About, AboutAdmin)