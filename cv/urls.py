from django.urls import path
from . import views


urlpatterns = [
     path('cv/', views.cv, name='cv'),
     path('cv-management/', views.cv_management,
          name='cv_management'),
     path('add-cv/', views.add_cv, name='add_cv'),
     path('edit-cv/<cv_id>/', views.edit_cv,
          name='edit_cv'),
     path('delete-cv/<cv_id>/', views.delete_cv,
          name='delete_cv'),
]