from django.urls import path
from .views import TaskListCreateView, TaskDetailView, TaskCompleteView

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:pk>/complete/', TaskCompleteView.as_view(), name='task-complete'),
]
