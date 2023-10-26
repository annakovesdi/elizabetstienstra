from django.contrib import admin
from .models import Info, Category


class InfoAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'date',
    )

    ordering = ('category', 'date')


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


admin.site.register(Info, InfoAdmin)
admin.site.register(Category, CategoryAdmin)
