from django.urls import path
from . import views


urlpatterns = [
     path('news/', views.news, name='news'),
     path('texts/', views.texts, name='texts'),
     path('info-management/', views.info_management,
          name='info_management'),
     path('add-info/', views.add_info, name='add_info'),
     path('edit-info/<info_id>/', views.edit_info,
          name='edit_info'),
     path('delete-info/<info_id>/', views.delete_info,
          name='delete_info'),
]