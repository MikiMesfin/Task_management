from django.urls import path
from .views import TaskListCreateView, TaskDetailView, UserCreateView
from .views import mark_task_complete, mark_task_incomplete
from .views import UserCreateView

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:pk>/complete/', mark_task_complete, name='mark-task-complete'),
    path('tasks/<int:pk>/incomplete/', mark_task_incomplete, name='mark-task-incomplete'),
    path('register/', UserCreateView.as_view(), name='user-register'),
]

