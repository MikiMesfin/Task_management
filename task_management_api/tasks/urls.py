from django.urls import path
from .views import TaskListCreateView, TaskDetailView, UserCreateView
from .views import mark_task_complete, mark_task_incomplete
from .views import UserCreateView
from . import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:pk>/complete/', mark_task_complete, name='mark-task-complete'),
    path('tasks/<int:pk>/incomplete/', mark_task_incomplete, name='mark-task-incomplete'),
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('', views.TaskListView.as_view(), name='task-list'),  # List of tasks
    path('create/', views.TaskCreateView.as_view(), name='task-create'),  # Create a new task
    path('<int:pk>/', views.TaskUpdateView.as_view(), name='task-detail'),  # Update/Edit task
    path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task-delete'),  # Delete task
    path('<int:pk>/complete/', views.mark_task_complete, name='mark-task-complete'),  # Mark task as complete
    path('<int:pk>/incomplete/', views.mark_task_incomplete, name='mark-task-incomplete'),  # Mark task as incomplete
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('register/', views.register, name='register'),
]
