from django.urls import path
from . import views


urlpatterns = [
    path('about/', views.about, name='about'),
    path('edit-about/', views.edit_about, name='edit_about'),
]