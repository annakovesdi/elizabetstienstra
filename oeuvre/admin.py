from django.contrib import admin
from .models import Work, Category, Image

# Register your models here.


class WorkAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'date',
        'materials',
    )

    ordering = ('category', 'date')


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )

class ImageAdmin(admin.ModelAdmin):
    list_display = (
        'image',
    )


admin.site.register(Work, WorkAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Image, ImageAdmin)
