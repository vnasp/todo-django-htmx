from django.urls import path
from .views import (
    HomeClass, DashboardView, EditTaskFormView,
    APIToggleTaskView, APICreateTaskView, APIUpdateTaskView, APIDeleteTaskView
)

urlpatterns = [
    path("", HomeClass.as_view(), name="home"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("edit-task/<int:task_id>/", EditTaskFormView.as_view(), name="edit_task"),
    
    path("api-htmx/tasks/create/", APICreateTaskView.as_view(), name="api_create_task"),
    path("api-htmx/tasks/<int:task_id>/toggle/", APIToggleTaskView.as_view(), name="api_toggle_task"),
    path("api-htmx/tasks/<int:task_id>/update/", APIUpdateTaskView.as_view(), name="api_update_task"),
    path("api-htmx/tasks/<int:task_id>/delete/", APIDeleteTaskView.as_view(), name="api_delete_task"),
]
