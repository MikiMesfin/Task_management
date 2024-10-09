from django.urls import path, include
from .views import mark_task_complete, mark_task_incomplete
from .views import TaskCreateView, RegisterView, TaskListView, TaskUpdateView, TaskDeleteView
from django.contrib.auth.views import LogoutView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Task-related views
    path('tasks/complete/<int:pk>/', mark_task_complete, name='mark-complete'),
    path('tasks/incomplete/<int:pk>/', mark_task_incomplete, name='mark-incomplete'),
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/update/<int:pk>/', TaskUpdateView.as_view(), name='task-update'),
    path('tasks/delete/<int:pk>/', TaskDeleteView.as_view(), name='task-delete'),

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
