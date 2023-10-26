from django.contrib import admin
from .models import Cv, Category


class CvAdmin(admin.ModelAdmin):
    list_display = (
        'category',
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


admin.site.register(Cv, CvAdmin)
admin.site.register(Category, CategoryAdmin)