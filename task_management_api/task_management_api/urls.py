"""
URL configuration for task_management_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from tasks.views import HomePageView, UserDetailView 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),  # Admin panel
    path('api/', include('tasks.urls')),           # API Page View
    path('', HomePageView.as_view(), name='home'),  # Home page view

    # API endpoints
    path('api/', include(('tasks.urls', 'tasks'), namespace='tasks')),
    path('api/users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT token obtain
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT token refresh

    # User management with Djoser
    path('users/', include('djoser.urls')),  
    path('users/', include('djoser.urls.authtoken')),  # If using token authentication

    # DRF session-based authentication routes (THIS IS CRITICAL)
    path('api-auth/', include('rest_framework.urls')),

    # Optional: Uncomment if you plan to use session-based authentication
    # path('api-auth/', include('rest_framework.urls')),  # For login/logout
]



