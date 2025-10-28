from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import TaskViewSet

# Router automático para ViewSets
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='tasks')

urlpatterns = [
    path('', include(router.urls)),
]
