from django.urls import path
from .views import HomeClass

app_name = 'tasks'

urlpatterns = [
    path('', HomeClass.as_view(), name='home'),
]
