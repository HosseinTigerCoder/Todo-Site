from django.urls import path
from . import views

urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('tasks/',views.TaskListView.as_view(),name='tasks'),
    path('toggle-check/<int:pk>',views.CheckTaskView.as_view(),name='check_task'),
    path('edit-task/<int:pk>',views.EditTaskView.as_view(),name='edit_task'),
    path('delete-task/<int:pk>',views.DeleteTaskView.as_view(),name='delete_task'),
    path('about/',views.about,name='about_us')
]