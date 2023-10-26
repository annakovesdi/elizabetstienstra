from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('home_management/', views.home_management, name='home_management'),
]