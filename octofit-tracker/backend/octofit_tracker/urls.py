"""octofit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
import os
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .views import (
    UserViewSet, TeamViewSet, ActivityViewSet,
    LeaderboardViewSet, WorkoutViewSet
)

# Get base URL based on environment
codespace_name = os.environ.get('CODESPACE_NAME')
if codespace_name:
    base_url = f"https://{codespace_name}-8000.app.github.dev"
else:
    base_url = "http://localhost:8000"

# Create router and register viewsets
router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'leaderboard', LeaderboardViewSet, basename='leaderboard')
router.register(r'workouts', WorkoutViewSet, basename='workout')


@api_view(['GET'])
def api_root(request, format=None):
    """
    API root endpoint that lists all available endpoints.
    """
    return Response({
        'message': 'Welcome to OctoFit Tracker API',
        'base_url': base_url,
        'endpoints': {
            'users': reverse('user-list', request=request, format=format),
            'teams': reverse('team-list', request=request, format=format),
            'activities': reverse('activity-list', request=request, format=format),
            'leaderboard': reverse('leaderboard-list', request=request, format=format),
            'workouts': reverse('workout-list', request=request, format=format),
        },
        'custom_endpoints': {
            'users_by_email': f'{base_url}/api/users/by_email/?email=<email>',
            'users_by_fitness_level': f'{base_url}/api/users/by_fitness_level/?level=<level>',
            'activities_by_user': f'{base_url}/api/activities/by_user/?user=<username>',
            'activities_by_type': f'{base_url}/api/activities/by_type/?type=<type>',
            'activities_recent': f'{base_url}/api/activities/recent/',
            'leaderboard_top': f'{base_url}/api/leaderboard/top/?limit=<N>',
            'leaderboard_by_team': f'{base_url}/api/leaderboard/by_team/?team=<team>',
            'workouts_by_difficulty': f'{base_url}/api/workouts/by_difficulty/?difficulty=<level>',
            'workouts_by_fitness_level': f'{base_url}/api/workouts/by_fitness_level/?level=<level>',
            'workouts_by_activity_type': f'{base_url}/api/workouts/by_activity_type/?type=<type>',
        }
    })


urlpatterns = [
    path('', api_root, name='root'),
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api-root'),
    path('api/', include(router.urls)),
]
