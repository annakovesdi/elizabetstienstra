from django.contrib import admin
from .models import Work, Category

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


admin.site.register(Work, WorkAdmin)
admin.site.register(Category, CategoryAdmin)
