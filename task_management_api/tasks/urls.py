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
    # API Home
    path('', APIHomeView.as_view(), name='api-home'),
    
    # Task Management
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'), 
    path('tasks/complete/<int:pk>/', mark_task_complete, name='mark-complete'),
    path('tasks/incomplete/<int:pk>/', mark_task_incomplete, name='mark-incomplete'),
    path('tasks/history/', TaskHistoryView.as_view(), name='task-history'),
    # path('tasks/drafts/', TaskDraftListView.as_view(), name='task-drafts'),
    
    # Category Management
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/update/', CategoryUpdateTemplateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', CategoryDeleteTemplateView.as_view(), name='category-delete'),
    
    # Authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='api_token_auth'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Include DRF authentication views
    path('api-auth/', include('rest_framework.urls')),
]
