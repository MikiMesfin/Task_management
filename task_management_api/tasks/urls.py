from django.urls import path, include
from .views import mark_task_complete, mark_task_incomplete
from .views import TaskListView, TaskCreateView, TaskUpdateView, TaskDetailView, CategoryTemplateView, TaskDeleteView, RegisterView
from django.contrib.auth.views import LogoutView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CategoryCreateView, CategoryTemplateView
from .views import (
    TaskListView,
    TaskCreateTemplateView,
    TaskDetailView,
    TaskUpdateTemplateView,
    TaskDeleteTemplateView,
    TaskHistoryView,
    CategoryCreateView,
    CategoryListView,
    CategoryCreateTemplateView,
    CategoryUpdateTemplateView,
    CategoryDeleteTemplateView,
    APIHomeView,
)


urlpatterns = [
    # Task-related views
    path('', APIHomeView.as_view(), name='api-home'),
    path('tasks/complete/<int:pk>/', mark_task_complete, name='mark-complete'),
    path('tasks/incomplete/<int:pk>/', mark_task_incomplete, name='mark-incomplete'),
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/create/', TaskCreateTemplateView.as_view(), name='task-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:pk>/update/', TaskUpdateTemplateView.as_view(), name='task-update'),
    path('tasks/<int:pk>/delete/', TaskDeleteTemplateView.as_view(), name='task-delete'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category-create'),
    path('categories/create/', CategoryCreateTemplateView.as_view(), name='category-create'),
    path('categories/<int:pk>/update/', CategoryUpdateTemplateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', CategoryDeleteTemplateView.as_view(), name='category-delete'),
    path('tasks/history/', TaskHistoryView.as_view(), name='task-history'),
    path('create/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/update/<int:pk>/', TaskUpdateView.as_view(), name='task-update'),


    # Authentication views
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('login/', obtain_auth_token, name='api_token_auth'),  # Token-based login (optional)
    path('api-auth/', include('rest_framework.urls')),  # For session login/logout

    # JWT authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Get access/refresh token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh token

    # User registration views
    path('register/', RegisterView.as_view(), name='register'),  # Registration page
    path('api/register/', RegisterView.as_view(), name='api-register'),  # API registration endpoint
]
