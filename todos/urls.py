from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_project, name='create_project'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path('projects/<int:project_id>/add_todo/', views.add_todo, name='add_todo'),
    path('todos/<int:todo_id>/complete/', views.mark_complete, name='mark_complete'),
    path('projects/<int:project_id>/export/', views.export_gist, name='export_gist'),
]
