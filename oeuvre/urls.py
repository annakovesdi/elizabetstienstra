from django.urls import path
from . import views

# Create your views here.

urlpatterns = [
    path('', views.oeuvre, name='oeuvre'),
    path('oeuvre_management/', views.oeuvre_management, name='oeuvre_management'),
    path('add_work/', views.add_work, name='add_work'),
    path('edit_work/<work_id>/', views.edit_work, name='edit_work'),
    path('delete-work/<work_id>/', views.delete_work, name='delete_work'),
]