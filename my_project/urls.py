"""
URL configuration for my_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
# from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)
from user.views import RegisterView, LoginView,UserListView
from project_management.views import ProjectListCreateAPIView, ProjectDetailAPIView, ProjectAssignPermissionsAPIView, TaskListCreateAPIView, TaskDetailAPIView
from project_management import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),

    path('register/',RegisterView.as_view(), name='register_view'),
    path('login/',LoginView.as_view(), name='login_view'),
    path('api/users/', UserListView.as_view(), name='get_users_list'),

    path('projects/', ProjectListCreateAPIView.as_view(), name='project-list-create'),
    path('projects/<int:pk>/', ProjectDetailAPIView.as_view(), name='project-detail'),
    path('projects/<int:pk>/add_user/', ProjectDetailAPIView.as_view(), name='project-add-user'),
    path('projects/<int:pk>/assign_permissions/', ProjectAssignPermissionsAPIView.as_view(), name='project-assign-permissions'),

    path('tasks/', TaskListCreateAPIView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailAPIView.as_view(), name='task-detail'),
]


urlpatterns += staticfiles_urlpatterns()